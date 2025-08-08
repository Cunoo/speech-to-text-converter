
import whisper
import yt_dlp
import tempfile
import os
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechToTextModel:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = None
        self._load_model()
        
    def _load_model(self):
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)
            logger.info("Model loaded succesfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise Exception(f"Failed to load model: {e}")
    
    def download_youtube_audio(self, youtube_url: str) -> Tuple[str, str]:
        try:
            logger.info(f"Downloading audio from: {youtube_url}")
            
            temp_dir = tempfile.gettempdir()
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
                'quiet': True,  # Suppress yt-dlp output
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                video_title = info.get('title', 'Unknown Title')
                video_duration = info.get('duration', 0)
                
                #Find the downloaded file
                audio_file_path = None
                for file in os.listdir(temp_dir):
                    if file.endswith('.wav'):
                        audio_file_path = os.path.join(temp_dir, file)
                        break
                if not audio_file_path:
                    raise Exception("No audio file found after download")
                
                logger.info(f"Audio downloaded succesfully: {video_title}")
                return audio_file_path, video_title, video_duration
            
        except Exception as e:
            logger.error(f"Error creating temporary directory: {e}")
            raise Exception(f"Failed to create temporary directory: {e}")
        
    def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> dict:
        try:
            logger.info(f"Starting transcription for {audio_path}")
            if not self.model:
                raise Exception("Model is not loaded")
            
            #Transcribe with optional language
            transcribe_options = {}
            if language:
                transcribe_options['language'] = language
                
            result = self.model.transcribe(audio=audio_path, **transcribe_options)
            
            transcription_result = {
                'text': result.get('text', '').strip(),
                'language': result.get('language', 'unknown'),
                'segments': result.get('segments', []),
                'confidence': self._calculate_average_confidence(result.get('segments', []))
            }
            
            logger.info("Transcription completed successfully")
            return transcription_result
            
        except Exception as e:
            logger.error(f"Error in transcription: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")
        
    def _calculate_average_confidence(self, segments: list) -> float:
        if not segments:
            return 0.0
        
        confidences = []
        for segment in segments:
            if 'avg_logprob' in segment:
                # Convert log probability to confidence (approximate)
                confidence = max(0.0, min(1.0, (segment['avg_logprob'] + 1.0)))
                confidences.append(confidence)
        
        return sum(confidences) / len(confidences) if confidences else 0.0
    
    def transcribe_youtube_video(self, youtube_url: str, language: Optional[str] = None) -> dict:
        audio_path = None
        try:
            # Download audio
            audio_path, video_title, duration = self.download_youtube_audio(youtube_url)
            
            # Transcribe audio
            transcription_result = self.transcribe_audio(audio_path, language)
            
            # Add metadata
            transcription_result.update({
                'video_title': video_title,
                'duration': duration,
                'source_url': youtube_url,
                'model_used': self.model_size
            })
            
            return transcription_result
            
        except Exception as e:
            logger.error(f"Error in YouTube transcription pipeline: {str(e)}")
            raise
        finally:
            # Clean up temporary files
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                    # Remove temporary directory if empty
                    temp_dir = os.path.dirname(audio_path)
                    if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                        os.rmdir(temp_dir)
                except Exception as cleanup_error:
                    logger.warning(f"Error cleaning up temporary files: {cleanup_error}")
    
    def transcribe_file(self, file_path: str, language: Optional[str] = None) -> dict:
        try:
            if not os.path.exists(file_path):
                raise Exception(f"Audio file not found: {file_path}")
            
            transcription_result = self.transcribe_audio(file_path, language)
            
            # Add file metadata
            transcription_result.update({
                'source_file': os.path.basename(file_path),
                'file_size': os.path.getsize(file_path),
                'model_used': self.model_size
            })
            
            return transcription_result
            
        except Exception as e:
            logger.error(f"Error transcribing file: {str(e)}")
            raise
    
    def get_model_info(self) -> dict:
        return {
            'model_size': self.model_size,
            'model_loaded': self.model is not None,
            'supported_languages': [
                'en', 'zh', 'de', 'es', 'ru', 'ko', 'fr', 'ja', 'pt', 'tr', 
                'pl', 'ca', 'nl', 'ar', 'sv', 'it', 'id', 'hi', 'fi', 'vi',
                'he', 'uk', 'el', 'ms', 'cs', 'ro', 'da', 'hu', 'ta', 'no'
            ]
        }

# Utility function to create model instance
def create_speech_model(model_size: str = "base") -> SpeechToTextModel:
    return SpeechToTextModel(model_size=model_size)
    
        