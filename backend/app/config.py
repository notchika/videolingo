from pathlib import Path

# --- Storage ---
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "storage" / "uploads"
OUTPUT_DIR = BASE_DIR / "storage" / "outputs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Limits ---
MAX_VIDEO_SECONDS = 10 * 60  # 10 minute cap
MAX_UPLOAD_BYTES = 500 * 1024 * 1024  # 500MB safety ceiling on file size
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".avi"}

# --- Models ---
WHISPER_MODEL_SIZE = "base"  # matches the scripture-detector setup; upgrade to "small"/"medium" if accuracy needs it
WHISPER_COMPUTE_TYPE = "int8"  # fast on CPU
NLLB_MODEL_NAME = "facebook/nllb-200-distilled-600M"  # good accuracy/speed tradeoff for local inference

# --- Supported languages ---
# code: (display name, NLLB FLORES-200 code, Whisper-supported-as-source flag)
LANGUAGES = {
    "en": {"name": "English",              "nllb": "eng_Latn", "whisper_source_ok": True},
    "fr": {"name": "French",               "nllb": "fra_Latn", "whisper_source_ok": True},
    "es": {"name": "Spanish",              "nllb": "spa_Latn", "whisper_source_ok": True},
    "pt": {"name": "Portuguese",           "nllb": "por_Latn", "whisper_source_ok": True},
    "de": {"name": "German",               "nllb": "deu_Latn", "whisper_source_ok": True},
    "ar": {"name": "Arabic",               "nllb": "arb_Arab", "whisper_source_ok": True},
    "hi": {"name": "Hindi",                "nllb": "hin_Deva", "whisper_source_ok": True},
    "zh": {"name": "Chinese (Simplified)", "nllb": "zho_Hans", "whisper_source_ok": True},
    "yo": {"name": "Yoruba",               "nllb": "yor_Latn", "whisper_source_ok": True},
    "ig": {"name": "Igbo",                 "nllb": "ibo_Latn", "whisper_source_ok": False},  # not in Whisper's trained set
    "ha": {"name": "Hausa",                "nllb": "hau_Latn", "whisper_source_ok": True},
    "sw": {"name": "Swahili",              "nllb": "swh_Latn", "whisper_source_ok": True},
    "ru": {"name": "Russian",              "nllb": "rus_Cyrl", "whisper_source_ok": True},
    "ja": {"name": "Japanese",             "nllb": "jpn_Jpan", "whisper_source_ok": True},
    "ko": {"name": "Korean",               "nllb": "kor_Hang", "whisper_source_ok": True},
}

WHISPER_TO_NLLB = {code: info["nllb"] for code, info in LANGUAGES.items()}