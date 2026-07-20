from pathlib import Path
from typing import List
from app.pipeline.transcribe import Segment


def _format_srt_timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _format_vtt_timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def write_srt(segments: List[Segment], texts: List[str], out_path: Path) -> Path:
    lines = []
    for i, (seg, text) in enumerate(zip(segments, texts), start=1):
        lines.append(str(i))
        lines.append(f"{_format_srt_timestamp(seg.start)} --> {_format_srt_timestamp(seg.end)}")
        lines.append(text)
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def write_vtt(segments: List[Segment], texts: List[str], out_path: Path) -> Path:
    lines = ["WEBVTT", ""]
    for seg, text in zip(segments, texts):
        lines.append(f"{_format_vtt_timestamp(seg.start)} --> {_format_vtt_timestamp(seg.end)}")
        lines.append(text)
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path