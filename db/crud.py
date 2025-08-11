from contextlib import contextmanager
from sqlalchemy.orm import Session, selectinload
from .database import SessionLocal
from . import models

@contextmanager
def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_or_create(session: Session, model, name: str):
    instance = session.query(model).filter_by(name=name).first()
    if not instance:
        instance = model(name=name)
        session.add(instance)
        session.flush()
    return instance

def add_image(file_path: str, authors=None, tags=None, characters=None):
    authors = authors or []
    tags = tags or []
    characters = characters or []
    with get_session() as session:
        image = models.Image(file_path=file_path)
        session.add(image)
        session.flush()
        image.authors = [get_or_create(session, models.Author, a.strip()) for a in authors if a.strip()]
        image.tags = [get_or_create(session, models.Tag, t.strip()) for t in tags if t.strip()]
        image.characters = [get_or_create(session, models.Character, c.strip()) for c in characters if c.strip()]
        session.flush()
        return image

def update_image(image_id: int, new_authors=None, new_tags=None, new_characters=None):
    new_authors = new_authors or []
    new_tags = new_tags or []
    new_characters = new_characters or []
    with get_session() as session:
        image = session.get(models.Image, image_id)
        if not image:
            return None
        for name in new_authors:
            author = get_or_create(session, models.Author, name.strip())
            if author not in image.authors:
                image.authors.append(author)
        for name in new_tags:
            tag = get_or_create(session, models.Tag, name.strip())
            if tag not in image.tags:
                image.tags.append(tag)
        for name in new_characters:
            character = get_or_create(session, models.Character, name.strip())
            if character not in image.characters:
                image.characters.append(character)
        session.flush()
        return image


def add_tags(image_id: int, new_tags=None):
    """Добавить теги к изображению."""
    return update_image(image_id, new_tags=new_tags)


def remove_tag(image_id: int, tag_name: str):
    """Удалить тег у изображения."""
    with get_session() as session:
        image = session.get(models.Image, image_id)
        if not image:
            return None
        tag = session.query(models.Tag).filter_by(name=tag_name).first()
        if tag and tag in image.tags:
            image.tags.remove(tag)
        session.flush()
        return image

def search_by_author(author_name: str):
    with get_session() as session:
        return (
            session.query(models.Image)
            .options(
                selectinload(models.Image.authors),
                selectinload(models.Image.tags),
                selectinload(models.Image.characters),
            )
            .join(models.Image.authors)
            .filter(models.Author.name.ilike(f"%{author_name}%"))
            .all()
        )

def search_by_tag(tag_name: str):
    with get_session() as session:
        return (
            session.query(models.Image)
            .options(
                selectinload(models.Image.authors),
                selectinload(models.Image.tags),
                selectinload(models.Image.characters),
            )
            .join(models.Image.tags)
            .filter(models.Tag.name.ilike(f"%{tag_name}%"))
            .all()
        )

def search_by_character(character_name: str):
    with get_session() as session:
        return (
            session.query(models.Image)
            .options(
                selectinload(models.Image.authors),
                selectinload(models.Image.tags),
                selectinload(models.Image.characters),
            )
            .join(models.Image.characters)
            .filter(models.Character.name.ilike(f"%{character_name}%"))
            .all()
        )


def get_image(image_id: int):
    """Получить изображение по ID вместе с его связями."""
    with get_session() as session:
        return (
            session.query(models.Image)
            .options(
                selectinload(models.Image.authors),
                selectinload(models.Image.tags),
                selectinload(models.Image.characters),
            )
            .filter(models.Image.id == image_id)
            .first()
        )


def get_all_images():
    """Получить все изображения с отсортированными связями."""
    with get_session() as session:
        return (
            session.query(models.Image)
            .options(
                selectinload(models.Image.authors),
                selectinload(models.Image.tags),
                selectinload(models.Image.characters),
            )
            .order_by(models.Image.id)
            .all()
        )


def get_all_authors():
    """Получить список всех авторов."""
    with get_session() as session:
        return session.query(models.Author).order_by(models.Author.name).all()
