"""Пакет с моделями тегирования изображений."""
from .base import BaseTagger
from .anime import AnimeTagger
from .photo import PhotoTagger
from .document import DocumentTagger


def get_tagger(image_type: str) -> BaseTagger:
    """Фабрика по типу изображения."""
    if image_type == "anime":
        return AnimeTagger()
    if image_type == "photo":
        return PhotoTagger()
    if image_type == "document":
        return DocumentTagger()
    raise ValueError(f"Неизвестный тип изображения: {image_type}")

__all__ = ["BaseTagger", "get_tagger"]
