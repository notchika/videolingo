import ffmpeg
from pathlib import Path


def get_duration_seconds(media_path: Path) -> float:
    probe = ffmpeg.probe(str(media_path))
    return float(probe["format"]["duration"])


def extract_audio(media_path: Path, output_wav_path: Path) -> Path:
    """
    Extract mono 16kHz PCM WAV audio from a video or audio-only file.
    16kHz mono is what Whisper expects internally, so we do the resample here
    rather than making Whisper do it, which keeps ffmpeg as the single place
    audio format decisions live.
    """
    (
        ffmpeg
        .input(str(media_path))
        .output(str(output_wav_path), ac=1, ar=16000, format="wav")
        .overwrite_output()
        .run(quiet=True)
    )
    return output_wav_path