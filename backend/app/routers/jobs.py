from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.config import TARGET_LANGUAGES
from app.models import TranscribeRequest, JobStatusResponse
from app.jobs import get_job, run_pipeline

router = APIRouter()


@router.post("/process")
def start_processing(req: TranscribeRequest, background_tasks: BackgroundTasks):
    if req.target_language not in TARGET_LANGUAGES:
        raise HTTPException(400, f"Unknown target language '{req.target_language}'")

    job = get_job(req.job_id)
    if job is None:
        raise HTTPException(404, "Job not found")

    background_tasks.add_task(run_pipeline, req.job_id, req.target_language)
    return {"job_id": req.job_id, "status": "queued"}


@router.get("/status/{job_id}", response_model=JobStatusResponse)
def get_status(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(404, "Job not found")

    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        progress_message=job.progress_message,
        detected_source_language=job.detected_source_language,
        error=job.error,
        srt_ready=job.srt_path is not None,
        vtt_ready=job.vtt_path is not None,
    )