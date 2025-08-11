"""Обработчики поиска записей."""
from db import crud


def search_images_by_author(name: str):
    """Найти изображения по автору."""
    return crud.search_by_author(name)


def search_images_by_tag(name: str):
    """Найти изображения по тегу."""
    return crud.search_by_tag(name)


def search_images_by_character(name: str):
    """Найти изображения по персонажу."""
    return crud.search_by_character(name)
