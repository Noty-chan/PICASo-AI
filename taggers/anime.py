import os
from typing import List

from .base import BaseTagger

try:  # DeepDanbooru — опциональная зависимость
    import deepdanbooru as dd
except Exception:  # pragma: no cover - библиотека может отсутствовать
    dd = None


class AnimeTagger(BaseTagger):
    """Теггер для аниме-изображений (DeepDanbooru, WD 1.4 и др.)."""

    def __init__(self, model_path: str | None = None) -> None:
        self.model_name = os.getenv("ANIME_MODEL", "deepdanbooru")
        self.model_path = model_path or os.getenv("ANIME_MODEL_PATH")
        self.threshold = float(os.getenv("ANIME_TAGGER_THRESHOLD", 0.5))

        if self.model_name == "deepdanbooru" and dd and self.model_path:
            self.model = dd.project.load_model(self.model_path)
            self.tags = dd.project.load_tags(self.model_path)
        else:  # Заглушка, если модель недоступна
            self.model = None
            self.tags = None

    def suggest_tags(self, path: str) -> List[str]:
        if self.model and dd:
            image = dd.image.load_image_for_evaluate(path)
            result = dd.project.evaluate_image(self.model, self.tags, image)
            # Сортируем теги по убыванию вероятности
            tags_scores = sorted(result.items(), key=lambda x: x[1], reverse=True)
            top = tags_scores[:10]
            # Фильтруем теги по порогу, но гарантируем минимум 5 тегов
            filtered = [tag for tag, score in top if score >= self.threshold]
            if len(filtered) < 5:
                filtered = [tag for tag, _ in top][:5]
            return filtered
        # Fallback-результат
        return ["anime", "sample"]
