import os
from typing import List
from .base import BaseTagger

class PhotoTagger(BaseTagger):
    """Теггер для фотографий (CLIP или аналог)."""

    def __init__(self, model_path: str | None = None) -> None:
        self.model = os.getenv("PHOTO_MODEL", "clip")
        self.model_path = model_path or os.getenv("PHOTO_MODEL_PATH")

    def suggest_tags(self, path: str) -> List[str]:
        # Фиктивная реализация для примера.
        return ["photo", "sample"]
