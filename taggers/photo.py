import os
from typing import List

from .base import BaseTagger

try:
    from transformers import pipeline
except Exception:  # pragma: no cover - зависимость может отсутствовать
    pipeline = None


class PhotoTagger(BaseTagger):
    """Теггер для фотографий (CLIP/BLIP и т.п.)."""

    def __init__(self, model_path: str | None = None) -> None:
        model = os.getenv(
            "PHOTO_MODEL", "nlpconnect/vit-gpt2-image-captioning"
        )
        self.model_path = model_path or os.getenv("PHOTO_MODEL_PATH", model)
        if pipeline:
            self.captioner = pipeline("image-to-text", model=self.model_path)
        else:
            self.captioner = None

    def suggest_tags(self, path: str) -> List[str]:
        if self.captioner:
            caption = self.captioner(path)[0]["generated_text"]
            return [token.strip(",.") for token in caption.lower().split()]
        return ["photo", "sample"]
