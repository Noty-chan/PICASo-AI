import os
from typing import List
from .base import BaseTagger

class DocumentTagger(BaseTagger):
    """Теггер для документов (OCR/CLIP)."""

    def __init__(self, model_path: str | None = None) -> None:
        self.model = os.getenv("DOC_MODEL", "ocr_clip")
        self.model_path = model_path or os.getenv("DOC_MODEL_PATH")

    def suggest_tags(self, path: str) -> List[str]:
        # Фиктивная реализация для примера.
        return ["document", "sample"]
