"""Обработчики для работы с базой данных."""
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


def get_image(image_id: int):
    """Получить изображение по ID."""
    return crud.get_image(image_id)


def get_all_images():
    """Получить все изображения."""
    return crud.get_all_images()


def get_all_authors():
    """Получить всех авторов."""
    return crud.get_all_authors()

