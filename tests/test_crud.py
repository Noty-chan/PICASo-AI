import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import db.database as database
import db.crud as crud


@pytest.fixture(autouse=True)
def in_memory_db(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        future=True,
    )
    database.Base.metadata.create_all(bind=engine)
    monkeypatch.setattr(database, "SessionLocal", TestingSessionLocal)
    monkeypatch.setattr(crud, "SessionLocal", TestingSessionLocal)
    yield


def test_add_and_search_tags():
    image = crud.add_image("file1.png", tags=["cat", "cute"])
    assert sorted(t.name for t in image.tags) == ["cat", "cute"]

    results = crud.search_by_tag("cat")
    assert len(results) == 1
    assert results[0].file_path == "file1.png"


def test_add_tags_updates_image():
    image = crud.add_image("file2.png", tags=["old"])
    crud.add_tags(image.id, ["new"])

    updated = crud.get_image(image.id)
    assert sorted(t.name for t in updated.tags) == ["new", "old"]

    results = crud.search_by_tag("new")
    assert len(results) == 1 and results[0].id == image.id
