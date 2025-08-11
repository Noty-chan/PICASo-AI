import os
import re
from typing import List

from .base import BaseTagger

try:
    import pytesseract
    from PIL import Image
except Exception:  # pragma: no cover - зависимость может отсутствовать
    pytesseract = None
    Image = None


class DocumentTagger(BaseTagger):
    """Теггер для документов (OCR + извлечение ключевых слов)."""

    def __init__(self, model_path: str | None = None) -> None:
        self.lang = os.getenv("DOC_LANG", "eng")

    def suggest_tags(self, path: str) -> List[str]:
        if pytesseract and Image:
            text = pytesseract.image_to_string(Image.open(path), lang=self.lang)
            words = set(re.findall(r"[A-Za-zА-Яа-я0-9]{3,}", text.lower()))
            return list(words)
        return ["document", "sample"]
