"""Примеры обработчиков, работающих с базой данных через ORM."""
from typing import List
from db import crud


def add_image(file_path: str, authors: List[str], tags: List[str], characters: List[str]):
    """Добавить изображение и связанные сущности."""
    return crud.add_image(file_path, authors, tags, characters)


def update_image(image_id: int, authors=None, tags=None, characters=None):
    """Обновить связи для изображения."""
    return crud.update_image(image_id, authors, tags, characters)


def search_images_by_author(name: str):
    """Найти изображения по автору."""
    return crud.search_by_author(name)


def search_images_by_tag(name: str):
    """Найти изображения по тегу."""
    return crud.search_by_tag(name)


def search_images_by_character(name: str):
    """Найти изображения по персонажу."""
    return crud.search_by_character(name)
