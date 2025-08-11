"""Вспомогательные функции для работы с изображениями."""
from db import crud


def get_image(image_id: int):
    """Получить изображение по ID."""
    return crud.get_image(image_id)


def get_all_images():
    """Получить все изображения."""
    return crud.get_all_images()


def get_all_authors():
    """Получить всех авторов."""
    return crud.get_all_authors()
