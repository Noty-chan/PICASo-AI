import os

from telegram.ext import Application

from db.database import init_db
from bot import telegram
import config
from classifier import classify_image
from taggers import get_tagger


def run_bot(token: str) -> None:
    """Запустить Telegram-бота."""
    init_db()
    os.makedirs(config.PHOTOS_DIR, exist_ok=True)
    application = Application.builder().token(token).build()
    telegram.register_handlers(application)
    application.run_polling()


def run_console() -> None:
    """Тестовый режим без доступа к Telegram."""
    print("BOT_TOKEN не найден. Запуск в режиме отладки через консоль.")
    print("Введите путь к изображению или 'exit' для выхода:")
    while True:
        try:
            path = input("> ").strip()
        except EOFError:
            break
        if not path or path.lower() in {"exit", "quit"}:
            break
        if not os.path.isfile(path):
            print("Файл не найден, попробуйте снова.")
            continue
        image_type = classify_image(path)
        tagger = get_tagger(image_type)
        tags = tagger.suggest_tags(path)
        print(f"Тип: {image_type}\nТеги: {', '.join(tags)}")


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if token:
        run_bot(token)
    else:
        run_console()


if __name__ == "__main__":
    main()

