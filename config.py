import os

PHOTOS_DIR = os.getenv("PHOTOS_DIR", "photos")

DATA_DIR = os.getenv("DATA_DIR", "data")
DATA_ANIME_DIR = os.getenv("DATA_ANIME_DIR", os.path.join(DATA_DIR, "anime"))
DATA_PHOTOS_DIR = os.getenv("DATA_PHOTOS_DIR", os.path.join(DATA_DIR, "photos"))
DATA_DOCS_DIR = os.getenv("DATA_DOCS_DIR", os.path.join(DATA_DIR, "docs"))

CATEGORY_DIRS = {
    "anime": DATA_ANIME_DIR,
    "photo": DATA_PHOTOS_DIR,
    "document": DATA_DOCS_DIR,
}
