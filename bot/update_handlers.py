"""Обработчики обновления записей."""
from db import crud


def update_image(image_id: int, authors=None, tags=None, characters=None):
    """Обновить связи для изображения."""
    return crud.update_image(image_id, authors, tags, characters)
