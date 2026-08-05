from enum import Enum
from typing import Optional
from pydantic import BaseModel


class JobStatus(str, Enum):
    QUEUED = "queued"
    EXTRACTING_AUDIO = "extracting_audio"
    TRANSCRIBING = "transcribing"
    TRANSLATING = "translating"
    GENERATING_SUBTITLES = "generating_subtitles"
    DONE = "done"
    FAILED = "failed"


class UploadResponse(BaseModel):
    job_id: str
    filename: str
    duration_seconds: float


class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    progress_message: str
    detected_source_language: Optional[str] = None
    error: Optional[str] = None
    srt_ready: bool = False
    vtt_ready: bool = False


class TranscribeRequest(BaseModel):
    job_id: str
    target_language: str  # one of the TARGET_LANGUAGES keys in config.py