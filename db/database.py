import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Путь к БД настраивается через переменную окружения
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./photos.db")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)

Base = declarative_base()


def init_db():
    # Import models to create tables
    import db.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
