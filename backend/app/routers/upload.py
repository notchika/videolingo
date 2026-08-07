from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
import aiofiles

from app.config import (
    UPLOAD_DIR,
    MAX_MEDIA_SECONDS,
    MAX_UPLOAD_BYTES,
    ALLOWED_MEDIA_EXTENSIONS,
    TARGET_LANGUAGES,
)
from app.pipeline.audio_extract import get_duration_seconds
from app.models import UploadResponse
from app.jobs import create_job

router = APIRouter()


@router.get("/languages")
def list_languages():
    return [
        {"code": code, "name": name}
        for code, name in sorted(TARGET_LANGUAGES.items(), key=lambda x: x[1])
    ]


@router.post("/upload", response_model=UploadResponse)
async def upload_media(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_MEDIA_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type '{ext}'. Allowed: {sorted(ALLOWED_MEDIA_EXTENSIONS)}")

    job_temp_name = f"upload_{Path(file.filename).stem}{ext}"
    dest_path = UPLOAD_DIR / job_temp_name

    size = 0
    async with aiofiles.open(dest_path, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_UPLOAD_BYTES:
                await out.close()
                dest_path.unlink(missing_ok=True)
                raise HTTPException(400, f"File exceeds max upload size of {MAX_UPLOAD_BYTES // (1024*1024)}MB")
            await out.write(chunk)

    duration = get_duration_seconds(dest_path)
    if duration > MAX_MEDIA_SECONDS:
        dest_path.unlink(missing_ok=True)
        raise HTTPException(
            400,
            f"File is {duration/60:.1f} minutes long. Max allowed is {MAX_MEDIA_SECONDS // 60} minutes."
        )

    job = create_job(dest_path)
    return UploadResponse(job_id=job.id, filename=file.filename, duration_seconds=duration)