import uuid
import traceback
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass, field

from app.config import UPLOAD_DIR, OUTPUT_DIR, LANGUAGES
from app.models import JobStatus
from app.pipeline import audio_extract, transcribe, translate, subtitles


@dataclass
class Job:
    id: str
    video_path: Path
    status: JobStatus = JobStatus.QUEUED
    progress_message: str = "Queued"
    detected_source_language: Optional[str] = None
    error: Optional[str] = None
    srt_path: Optional[Path] = None
    vtt_path: Optional[Path] = None
    _segments: list = field(default_factory=list)


JOBS: Dict[str, Job] = {}


def create_job(video_path: Path) -> Job:
    job_id = str(uuid.uuid4())
    job = Job(id=job_id, video_path=video_path)
    JOBS[job_id] = job
    return job


def get_job(job_id: str) -> Optional[Job]:
    return JOBS.get(job_id)


def run_pipeline(job_id: str, target_language: str):
    """
    Runs synchronously inside a FastAPI BackgroundTask. For real concurrent load
    this should move to a proper task queue (Celery/RQ), but for a single-worker
    dev setup this is enough to keep uploads non-blocking.
    """
    job = JOBS[job_id]
    try:
        # 1. Extract audio
        job.status = JobStatus.EXTRACTING_AUDIO
        job.progress_message = "Extracting audio from video"
        wav_path = UPLOAD_DIR / f"{job_id}.wav"
        audio_extract.extract_audio(job.video_path, wav_path)

        # 2. Transcribe
        job.status = JobStatus.TRANSCRIBING
        job.progress_message = "Transcribing speech"
        segments, detected_lang = transcribe.transcribe(wav_path)
        job.detected_source_language = detected_lang
        job._segments = segments

        if not segments:
            raise ValueError("No speech detected in the audio track.")

        # 3. Translate
        job.status = JobStatus.TRANSLATING
        job.progress_message = f"Translating from {detected_lang} to {target_language}"
        source_nllb = LANGUAGES.get(detected_lang, {}).get("nllb")
        target_nllb = LANGUAGES[target_language]["nllb"]

        if source_nllb is None:
            # Whisper detected a language outside our 15-language map; fall back to
            # treating the transcript as-is (no translation) rather than failing the job.
            translated_texts = [s.text for s in segments]
        else:
            translated_texts = translate.translate_batch(
                [s.text for s in segments], source_nllb, target_nllb
            )

        # 4. Generate subtitle files
        job.status = JobStatus.GENERATING_SUBTITLES
        job.progress_message = "Generating subtitle files"
        srt_path = OUTPUT_DIR / f"{job_id}.srt"
        vtt_path = OUTPUT_DIR / f"{job_id}.vtt"
        subtitles.write_srt(segments, translated_texts, srt_path)
        subtitles.write_vtt(segments, translated_texts, vtt_path)
        job.srt_path = srt_path
        job.vtt_path = vtt_path

        job.status = JobStatus.DONE
        job.progress_message = "Done"

    except Exception as e:
        job.status = JobStatus.FAILED
        job.error = str(e)
        job.progress_message = "Failed"
        traceback.print_exc()