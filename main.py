import os

from telegram.ext import Application

from db.database import init_db
from bot import telegram


TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")


def main() -> None:
    init_db()
    os.makedirs('photos', exist_ok=True)
    application = Application.builder().token(TOKEN).build()
    telegram.register_handlers(application)
    application.run_polling()


if __name__ == "__main__":
    main()

