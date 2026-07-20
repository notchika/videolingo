from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.jobs import get_job

router = APIRouter()


@router.get("/download/{job_id}/srt")
def download_srt(job_id: str):
    job = get_job(job_id)
    if job is None or job.srt_path is None:
        raise HTTPException(404, "Subtitle file not ready")
    return FileResponse(job.srt_path, filename=f"{job_id}.srt", media_type="application/x-subrip")


@router.get("/download/{job_id}/vtt")
def download_vtt(job_id: str):
    job = get_job(job_id)
    if job is None or job.vtt_path is None:
        raise HTTPException(404, "Subtitle file not ready")
    return FileResponse(job.vtt_path, filename=f"{job_id}.vtt", media_type="text/vtt")