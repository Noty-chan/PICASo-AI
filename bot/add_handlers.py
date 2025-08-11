"""Обработчики добавления и управления тегами."""
from typing import List

from db import crud


def add_image(
    file_path: str,
    authors: List[str] | None = None,
    tags: List[str] | None = None,
    characters: List[str] | None = None,
):
    """Сохранить изображение и связанные сущности в БД."""
    authors = authors or []
    tags = tags or []
    characters = characters or []
    image = crud.add_image(file_path, authors, tags, characters)
    return image


def add_tags(image_id: int, tags: List[str]):
    """Ручное добавление тегов."""
    return crud.add_tags(image_id, tags)


def remove_tag(image_id: int, tag: str):
    """Удаление тега."""
    return crud.remove_tag(image_id, tag)
