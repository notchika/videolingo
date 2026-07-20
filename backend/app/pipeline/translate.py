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


def translate_batch(texts: List[str], source_nllb_code: str, target_nllb_code: str) -> List[str]:
    """
    Translates a list of text segments (e.g. subtitle lines) in one batched pass.
    Batching matters here: calling the model once per subtitle line is what kills
    throughput on a 10-minute video that might have 150+ segments.
    """
    if source_nllb_code == target_nllb_code:
        return texts

    tokenizer, model = _load()
    tokenizer.src_lang = source_nllb_code

    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(target_nllb_code)

    generated = model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_token_id,
        max_length=256,
    )
    return tokenizer.batch_decode(generated, skip_special_tokens=True)