from typing import List
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from app.config import NLLB_MODEL_NAME

_tokenizer = None
_model = None


def _load():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL_NAME)
    return _tokenizer, _model


CHUNK_SIZE = 24  # segments per translation batch


def translate_batch(texts: List[str], source_nllb_code: str, target_nllb_code: str) -> List[str]:
    """
    Translates a list of text segments (e.g. subtitle lines) in chunks rather than
    one giant batch. A single batch works fine for a 10-minute video (~150 segments),
    but a 25-minute video can have 300-400+, and padding them all to the same length
    in one forward pass risks a memory spike. Chunking keeps peak memory bounded
    regardless of video length, at the cost of a few more (still batched) model calls.
    """
    if source_nllb_code == target_nllb_code:
        return texts

    tokenizer, model = _load()
    tokenizer.src_lang = source_nllb_code
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(target_nllb_code)

    results: List[str] = []
    for i in range(0, len(texts), CHUNK_SIZE):
        chunk = texts[i:i + CHUNK_SIZE]
        inputs = tokenizer(chunk, return_tensors="pt", padding=True, truncation=True)
        generated = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=256,
        )
        results.extend(tokenizer.batch_decode(generated, skip_special_tokens=True))
    return results