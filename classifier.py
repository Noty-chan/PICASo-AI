import os
import shutil
from pathlib import Path
from typing import Tuple

from taggers import get_tagger, BaseTagger
import config

try:  # Опциональная зависимость для классификации CLIP
    import open_clip
    import torch
    from PIL import Image
except Exception:  # pragma: no cover - библиотека может отсутствовать
    open_clip = None
    torch = None
    Image = None

# Fallback-классификация по расширению файла
EXTENSION_MAP = {
    ".png": "anime",
    ".jpg": "photo",
    ".jpeg": "photo",
    ".gif": "anime",
    ".pdf": "document",
}

MODEL_NAME = os.getenv("CLASSIFIER_MODEL", "ViT-B-32")
MODEL_WEIGHTS = os.getenv("CLASSIFIER_MODEL_PATH", "openai")

_model = None
_preprocess = None
_tokenizer = None


def _load_classifier():
    """Лениво загрузить модель CLIP, если она доступна."""
    global _model, _preprocess, _tokenizer
    if open_clip is None or torch is None or Image is None:
        return None, None, None
    if _model is None:
        _model, _preprocess = open_clip.create_model_and_transforms(
            MODEL_NAME, pretrained=MODEL_WEIGHTS
        )
        _tokenizer = open_clip.get_tokenizer(MODEL_NAME)
    return _model, _preprocess, _tokenizer


def classify_image(path: str) -> str:
    """Определить тип изображения с помощью CLIP (или по расширению)."""
    model, preprocess, tokenizer = _load_classifier()
    if not model:
        suffix = Path(path).suffix.lower()
        return EXTENSION_MAP.get(suffix, "photo")

    image = preprocess(Image.open(path)).unsqueeze(0)
    text = tokenizer(["anime", "photo", "document"])
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        logits = (image_features @ text_features.T)[0]
    categories = ["anime", "photo", "document"]
    return categories[int(logits.argmax())]


def move_to_category(path: str, image_type: str) -> str:
    """Переместить файл в директорию по типу."""
    mapping = config.CATEGORY_DIRS
    target_dir = Path(mapping[image_type])
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / Path(path).name
    shutil.move(path, destination)
    return str(destination)


def prepare_image(path: str) -> Tuple[str, BaseTagger]:
    """Классифицировать изображение, переместить и вернуть путь вместе с теггером."""
    image_type = classify_image(path)
    new_path = move_to_category(path, image_type)
    tagger = get_tagger(image_type)
    return new_path, tagger
