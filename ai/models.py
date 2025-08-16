from typing import Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class JobStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class TranscriptRequest(BaseModel):
    user_id : int = Field(..., description="user id from spring")
    youtube_url: str = Field(..., description="YouTube video URL")
    language: Optional[str] = Field(None, description="Language code (e.g., 'en', 'es')")
    
class FileTranscriptionRequest(BaseModel):
    user_id: int = Field(..., description="user id from spring")
    file_path: str = Field(..., description="Path to audio file")
    language: Optional[str] = Field(None, description="Language code")
    

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    message: str
    user_id: int
    
class JobStatusResponse(BaseModel):
    job_id: str
    user_id: int
    status: JobStatus
    progress: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None
    queue_position: Optional[int] = None
    estimated_wait_time: Optional[str] = None
    

class JobListResponse(BaseModel): #Monitoring
    jobs: list[Dict[str, Any]]
    total: int
    by_status: Dict[str, int]
    
class UserJobsResponse(BaseModel):
    user_id: int
    jobs: list[Dict[str, Any]]
    total: int
    active: int
    completed: int
    
class SystemStatsResponse(BaseModel):
    system: Dict[str, Any]
    service: Dict[str, Any]
    jobs: Dict[str, Any]
    
class SpringTranscriptResponse(BaseModel):
    message: str
    status: str
    video_id: Optional[int] = None
    job_id: Optional[str] = None
    transcription: Optional[str] = None