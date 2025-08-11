import shutil
from pathlib import Path
from typing import Tuple
from taggers import get_tagger, BaseTagger

# Простая классификация по расширению файла. В реальном проекте здесь может
# использоваться модель CLIP или иная нейросеть.
EXTENSION_MAP = {
    ".png": "anime",
    ".jpg": "photo",
    ".jpeg": "photo",
    ".gif": "anime",
    ".pdf": "document",
}


def classify_image(path: str) -> str:
    """Определить тип изображения по расширению файла."""
    suffix = Path(path).suffix.lower()
    return EXTENSION_MAP.get(suffix, "photo")


def move_to_category(path: str, image_type: str) -> str:
    """Переместить файл в директорию по типу."""
    mapping = {"anime": "data/anime", "photo": "data/photos", "document": "data/docs"}
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
