from abc import ABC, abstractmethod
from typing import List

class BaseTagger(ABC):
    """Абстрактный класс для моделей тегирования изображений."""

    @abstractmethod
    def suggest_tags(self, path: str) -> List[str]:
        """Возвращает список предложенных тегов для изображения по указанному пути."""
        raise NotImplementedError
