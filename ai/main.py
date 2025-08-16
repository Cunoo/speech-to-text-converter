from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging
from contextlib import asynccontextmanager
from models import (
    TranscriptRequest, JobResponse, JobStatusResponse, 
    JobStatus, UserJobsResponse, SystemStatsResponse
)
from speech_model import SpeechToTextModel, create_speech_model
import os
from collections import defaultdict, deque
import psutil
import gc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state management
MAX_CONCURRENT_JOBS = 4
WHISPER_MODEL_SIZE = "small"
MAX_QUEUE_SIZE = 50

class JobManager:
    def __init__(self):
        self.jobs: Dict[str, Dict] = {}
        self.job_queue: deque = deque()
        self.user_jobs: Dict[int, list] = defaultdict(list)
        self.active_jobs = set()
        
        self.max_concurrent = int(os.getenv("MAX_CONCURRENT_JOBS", 4))
        self.max_queue_size = int(os.getenv("MAX_QUEUE_SIZE", 50))
        self.processing_lock = asyncio.Lock() 
        
    async def add_job(self, job_id: str, user_id: int, request_data: dict) -> bool: 
        if len(self.job_queue) >= self.max_queue_size:
            return False
        
        job = {
            'job_id': job_id,
            'user_id': user_id,
            'status': JobStatus.PENDING,
            'created_at': datetime.utcnow().isoformat(),
            'request_data': request_data,
            'progress': 'Queued',
            'queue_position': len(self.job_queue) + 1
        }
        self.jobs[job_id] = job
        self.job_queue.append(job_id)
        self.user_jobs[user_id].append(job_id)
        

        asyncio.create_task(self._process_queue())
        return True
    
    async def _process_queue(self):
        async with self.processing_lock:
            while (len(self.active_jobs) < self.max_concurrent and self.job_queue):
                
                job_id = self.job_queue.popleft()
                if job_id in self.jobs:
                    self.active_jobs.add(job_id)
                    self.jobs[job_id]['status'] = JobStatus.IN_PROGRESS
                    self.jobs[job_id]['progress'] = 'In progress...'
                    
                    # Update queue position
                    for i, remaining_job_id in enumerate(self.job_queue):
                        if remaining_job_id in self.jobs:
                            self.jobs[remaining_job_id]['queue_position'] = i + 1
                        
                    # Process job in background
                    asyncio.create_task(self._process_job(job_id))
                    
    async def _process_job(self, job_id: str):
        try:
            job = self.jobs[job_id]  
            request_data = job['request_data']
            
            # Instantiate model if not loaded
            if not hasattr(self, 'speech_model') or not self.speech_model:
                self.speech_model = create_speech_model(
                    model_size=os.getenv("WHISPER_MODEL_SIZE", WHISPER_MODEL_SIZE))
            
            # Process transcription
            if 'youtube_url' in request_data:
                result = await asyncio.to_thread(
                    self.speech_model.transcribe_youtube_video,
                    request_data['youtube_url'],
                    request_data.get('language')
                )
            else:
                result = await asyncio.to_thread(
                    self.speech_model.transcribe_file,
                    request_data['file_path'],
                    request_data.get('language')
                )
            
            # Update job status
            self.jobs[job_id].update({
                'status': JobStatus.COMPLETED,
                'completed_at': datetime.utcnow().isoformat(),
                'progress': 'Completed',
                'result': result
            })
            
            # Notify spring boot backend
            await self._notify_spring_backend(job_id, result)
            
        except Exception as e:
            logger.error(f"Job {job_id} failed: {str(e)}")
            self.jobs[job_id].update({
                'status': JobStatus.FAILED,
                'completed_at': datetime.utcnow().isoformat(),
                'error': str(e),
                'progress': 'Failed'
            })
        finally:
            self.active_jobs.discard(job_id)
            asyncio.create_task(self._process_queue())
            
            await self._cleanup_old_jobs(job_id)
            
    async def _notify_spring_backend(self, job_id: str, result: dict):
        """Notify Spring Boot when transcription is complete"""
        import aiohttp
        
        spring_url = os.getenv('SPRING_BACKEND_URL', 'http://localhost:8080')
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    'jobId': job_id,
                    'status': 'completed',
                    'transcription': result.get('text', ''),
                    'videoTitle': result.get('video_title', ''),
                    'duration': result.get('duration', 0)
                }
                
                async with session.post(
                    f"{spring_url}/api/transcript/complete",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status != 200:
                        logger.warning(f"Failed to notify Spring backend: {response.status}")
        except Exception as e:
            logger.error(f"Error notifying Spring backend: {e}")
    
    async def _cleanup_old_jobs(self, current_job_id: str):
        """Keep memory usage low by cleaning old jobs"""
        job = self.jobs.get(current_job_id)
        if not job:
            return
            
        user_id = job['user_id']
        user_job_list = self.user_jobs[user_id]
        
        # Keep only last 20 jobs per user
        if len(user_job_list) > 20:
            jobs_to_remove = user_job_list[:-20]
            for old_job_id in jobs_to_remove:
                self.jobs.pop(old_job_id, None)
            self.user_jobs[user_id] = user_job_list[-20:]
    
    def get_job_status(self, job_id: str) -> Optional[dict]:
        return self.jobs.get(job_id)
    
    def get_user_jobs(self, user_id: int) -> list:
        job_ids = self.user_jobs.get(user_id, [])
        return [self.jobs[job_id] for job_id in job_ids if job_id in self.jobs]
    
    def get_system_stats(self) -> dict:
        total_jobs = len(self.jobs)
        by_status = defaultdict(int)
        for job in self.jobs.values():
            by_status[job['status']] += 1
            
        return {
            'system': {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'active_jobs': len(self.active_jobs),
                'queued_jobs': len(self.job_queue)
            },
            'service': {
                'max_concurrent': self.max_concurrent,
                'max_queue_size': self.max_queue_size,
                'model_loaded': hasattr(self, 'speech_model') and self.speech_model is not None
            },
            'jobs': {
                'total': total_jobs,
                'by_status': dict(by_status)
            }
        }

# Global job manager
job_manager = JobManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting FastAPI transcription service")
    
    # Cleanup task every 10 minutes
    async def periodic_cleanup():
        while True:
            try:
                await asyncio.sleep(600)  # 10 minutes
                gc.collect()  # Force garbage collection
                
                # Remove jobs older than 1 hour
                cutoff_time = datetime.utcnow() - timedelta(hours=1)
                jobs_to_remove = []
                
                for job_id, job in job_manager.jobs.items():
                    created_at = datetime.fromisoformat(job['created_at'])
                    if created_at < cutoff_time and job['status'] in [JobStatus.COMPLETED, JobStatus.FAILED]:
                        jobs_to_remove.append(job_id)
                
                for job_id in jobs_to_remove:
                    user_id = job_manager.jobs[job_id]['user_id']
                    job_manager.jobs.pop(job_id, None)
                    if job_id in job_manager.user_jobs[user_id]:
                        job_manager.user_jobs[user_id].remove(job_id)
                
                if jobs_to_remove:
                    logger.info(f"Cleaned up {len(jobs_to_remove)} old jobs")
                    
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")
    
    cleanup_task = asyncio.create_task(periodic_cleanup())
    
    yield
    
    # Shutdown
    cleanup_task.cancel()
    logger.info("Shutting down transcription service")

app = FastAPI(
    title="MindAura AI Transcription Service",
    description="AI-powered speech transcription with job queue system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('ALLOWED_ORIGINS', '*').split(','),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.post("/transcribe/youtube", response_model=JobResponse)
async def transcribe_youtube(request: TranscriptRequest):
    """Submit YouTube transcription job"""
    
    # Rate limiting per user (optional)
    user_jobs = job_manager.get_user_jobs(request.user_id)
    active_jobs = [j for j in user_jobs if j['status'] in [JobStatus.PENDING, JobStatus.IN_PROGRESS]]  # ✅ Fixed status
    
    if len(active_jobs) >= 3:  # Max 3 active jobs per user
        raise HTTPException(
            status_code=429,
            detail="Too many active jobs. Please wait for current jobs to complete."
        )
    
    job_id = str(uuid.uuid4())[:8] 
    
    success = await job_manager.add_job(
        job_id=job_id,
        user_id=request.user_id,
        request_data={
            'youtube_url': request.youtube_url,
            'language': request.language
        }
    )
    
    if not success:
        raise HTTPException(
            status_code=503,
            detail="Service is at capacity. Please try again later."
        )
    
    return JobResponse(
        job_id=job_id,
        status=JobStatus.PENDING,
        message="Job queued successfully",
        user_id=request.user_id
    )

@app.get("/job/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get job status and results"""
    job = job_manager.get_job_status(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Estimate wait time for queued jobs
    estimated_wait = None
    if job['status'] == JobStatus.PENDING:
        position = job.get('queue_position', 0)
        estimated_wait = f"~{position * 2} minutes"  # Rough estimate
    
    return JobStatusResponse(
        job_id=job['job_id'],
        user_id=job['user_id'],
        status=job['status'],
        progress=job.get('progress'),
        result=job.get('result'),
        error=job.get('error'),
        created_at=job['created_at'],
        completed_at=job.get('completed_at'),
        queue_position=job.get('queue_position'),
        estimated_wait_time=estimated_wait
    )

@app.get("/user/{user_id}/jobs", response_model=UserJobsResponse)
async def get_user_jobs(user_id: int):
    """Get all jobs for a specific user"""
    jobs = job_manager.get_user_jobs(user_id)
    
    active_count = len([j for j in jobs if j['status'] in [JobStatus.PENDING, JobStatus.IN_PROGRESS]])
    completed_count = len([j for j in jobs if j['status'] == JobStatus.COMPLETED])
    
    return UserJobsResponse(
        user_id=user_id,
        jobs=jobs,
        total=len(jobs),
        active=active_count,
        completed=completed_count
    )

@app.get("/system/stats", response_model=SystemStatsResponse)
async def get_system_stats():
    """Get system statistics (for monitoring)"""
    return SystemStatsResponse(**job_manager.get_system_stats())

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    stats = job_manager.get_system_stats()
    
    if stats['system']['memory_percent'] > 90:
        raise HTTPException(status_code=503, detail="High memory usage")
    
    return {
        "status": "healthy",
        "active_jobs": stats['system']['active_jobs'],
        "queued_jobs": stats['system']['queued_jobs']
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        workers=1  # Important: single worker for shared state
    )