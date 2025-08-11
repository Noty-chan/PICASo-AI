from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

image_author = Table(
    'image_author',
    Base.metadata,
    Column('image_id', ForeignKey('images.id'), primary_key=True),
    Column('author_id', ForeignKey('authors.id'), primary_key=True),
)

image_tag = Table(
    'image_tag',
    Base.metadata,
    Column('image_id', ForeignKey('images.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)

image_character = Table(
    'image_character',
    Base.metadata,
    Column('image_id', ForeignKey('images.id'), primary_key=True),
    Column('character_id', ForeignKey('characters.id'), primary_key=True),
)


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, unique=True, nullable=False)

    authors = relationship('Author', secondary=image_author, back_populates='images')
    tags = relationship('Tag', secondary=image_tag, back_populates='images')
    characters = relationship('Character', secondary=image_character, back_populates='images')


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    images = relationship('Image', secondary=image_author, back_populates='authors')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    images = relationship('Image', secondary=image_tag, back_populates='tags')


class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    images = relationship('Image', secondary=image_character, back_populates='characters')
