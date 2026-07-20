from pathlib import Path
from dataclasses import dataclass
from typing import List
from faster_whisper import WhisperModel

from app.config import WHISPER_MODEL_SIZE, WHISPER_COMPUTE_TYPE

_model: WhisperModel | None = None


def get_model() -> WhisperModel:
    """Lazy singleton so the model loads once per process, not once per request."""
    global _model
    if _model is None:
        _model = WhisperModel(WHISPER_MODEL_SIZE, compute_type=WHISPER_COMPUTE_TYPE)
    return _model


@dataclass
class Segment:
    start: float
    end: float
    text: str


def transcribe(audio_path: Path) -> tuple[List[Segment], str]:
    """
    Returns (segments, detected_language_code).
    beam_size=5 is a balanced default for CPU inference - the scripture detector's
    beam_size=7 pushed latency higher than a batch web job needs.
    """
    model = get_model()
    segments_iter, info = model.transcribe(
        str(audio_path),
        beam_size=5,
        vad_filter=True,  # skip silence rather than time-slicing on a fixed timer
    )
    segments = [Segment(start=s.start, end=s.end, text=s.text.strip()) for s in segments_iter]
    return segments, info.language