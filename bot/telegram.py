import os
import config
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    CallbackContext,
    ConversationHandler,
)
from . import handlers
from classifier import prepare_image

# Определяем состояния для ConversationHandler
ADD_PHOTO, ADD_AUTHORS, ADD_TAGS, ADD_CHARACTERS = range(4)
UPDATE_ID, UPDATE_AUTHORS, UPDATE_TAGS, UPDATE_CHARACTERS = range(4, 8)


# Функция для создания меню команд
def create_command_menu():
    command_menu = [
        ["/add➕", "/update⬆️"],
        ["/search_author👤", "/search_tag🔖"],
        ["/search_character👥", "/display📱"],
        ["/tag_add➕", "/tag_remove➖"],
        ["/search_author_list📋", "/help🆘"],
    ]
    return ReplyKeyboardMarkup(command_menu, resize_keyboard=True, one_time_keyboard=True)


# Функция для создания инлайн-кнопок для пролистывания
def create_navigation_buttons(current_index, total):
    keyboard = []
    if current_index > 0:
        keyboard.append(InlineKeyboardButton("⬅️ Предыдущая", callback_data=f"prev_{current_index}"))
    if current_index < total - 1:
        keyboard.append(InlineKeyboardButton("Следующая ➡️", callback_data=f"next_{current_index}"))
    return InlineKeyboardMarkup([keyboard] if keyboard else [])


def create_author_navigation_buttons(current_index, total):
    keyboard = []
    if current_index > 0:
        keyboard.append(InlineKeyboardButton("⬅️ Предыдущий", callback_data=f"author_prev_{current_index}"))
    if current_index < total - 1:
        keyboard.append(InlineKeyboardButton("Следующий ➡️", callback_data=f"author_next_{current_index}"))
    return InlineKeyboardMarkup([keyboard] if keyboard else [])


# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "🌟 <b>Привет! Я бот для управления базой данных фотографий.</b>\n\n"
        "Используй команды:\n"
        "/add - Добавить новую фотографию\n"
        "/update - Обновить запись\n"
        "/search_author - Найти по автору\n"
        "/search_tag - Найти по тегу\n"
        "/search_character - Найти по персонажу\n"
        "/tag_add - Добавить теги к записи\n"
        "/tag_remove - Удалить тег из записи\n"

        "/search_author_list - Список всех авторов\n"
        "/display - Показать все записи\n"
        "/help - Показать список команд",
        parse_mode="HTML",
        reply_markup=create_command_menu()
    )


# Команда /add
async def add_entry(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("📸 Отправьте фотографию:")
    return ADD_PHOTO


async def add_photo(update: Update, context: CallbackContext) -> int:
    if not update.message.photo:
        await update.message.reply_text("❌ Пожалуйста, отправьте фотографию.")
        return ADD_PHOTO
    photo = update.message.photo[-1]  # Берем фото наибольшего размера
    file = await context.bot.get_file(photo.file_id)
    raw_path = os.path.join(config.PHOTOS_DIR, f"{photo.file_unique_id}.jpg")
    os.makedirs(config.PHOTOS_DIR, exist_ok=True)
    await file.download_to_drive(raw_path)
    new_path, tagger = prepare_image(raw_path)
    suggested_tags = tagger.suggest_tags(new_path)
    context.user_data['file_path'] = new_path
    context.user_data['suggested_tags'] = suggested_tags
    await update.message.reply_text("👤 Введите автора (через запятую, если несколько):")
    return ADD_AUTHORS


async def add_authors(update: Update, context: CallbackContext) -> int:
    context.user_data['authors'] = [author.strip() for author in update.message.text.split(',')]
    suggested = context.user_data.get('suggested_tags', [])
    suggested_str = ', '.join(suggested)
    await update.message.reply_text(
        f"🏷️ Предложенные теги: {suggested_str}\nОтредактируйте или добавьте свои (через запятую):"
    )
    return ADD_TAGS


async def add_tags(update: Update, context: CallbackContext) -> int:
    context.user_data['tags'] = [tag.strip() for tag in update.message.text.split(',') if tag.strip()]
    await update.message.reply_text("👥 Введите персонажей (через запятую):")
    return ADD_CHARACTERS


async def add_characters(update: Update, context: CallbackContext) -> int:
    context.user_data['characters'] = [
        character.strip() for character in update.message.text.split(',') if character.strip()
    ]
    tags = set(context.user_data.get('suggested_tags', []))
    tags.update(context.user_data.get('tags', []))
    handlers.add_image(
        context.user_data['file_path'],
        context.user_data.get('authors'),
        list(tags),
        context.user_data['characters'],
    )
    await update.message.reply_text("✅ Фотография добавлена!", parse_mode="HTML")
    return ConversationHandler.END


# Команда /update
async def update_entry(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Введите ID записи, которую хотите обновить:")
    return UPDATE_ID


async def update_id(update: Update, context: CallbackContext) -> int:
    try:
        entry_id = int(update.message.text)
        image = handlers.get_image(entry_id)
        if not image:
            await update.message.reply_text("❌ Запись с таким ID не найдена. Введите другой ID:")
            return UPDATE_ID
        context.user_data['id'] = entry_id
        await update.message.reply_text(
            "Введите новых авторов (через запятую, или нажмите /skip, чтобы оставить старых):")
        return UPDATE_AUTHORS
    except ValueError:
        await update.message.reply_text("❌ Пожалуйста, введите числовой ID:")
        return UPDATE_ID


async def update_authors(update: Update, context: CallbackContext) -> int:
    if update.message.text != "/skip":
        context.user_data['new_authors'] = [author.strip() for author in update.message.text.split(',')]
    await update.message.reply_text("Введите новые теги (через запятую, или нажмите /skip, чтобы оставить старые):")
    return UPDATE_TAGS


async def update_authors_skip(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Введите новые теги (через запятую, или нажмите /skip, чтобы оставить старые):")
    return UPDATE_TAGS


async def update_tags(update: Update, context: CallbackContext) -> int:
    if update.message.text != "/skip":
        context.user_data['new_tags'] = [tag.strip() for tag in update.message.text.split(',')]
    await update.message.reply_text(
        "Введите новых персонажей (через запятую, или нажмите /skip, чтобы оставить старых):")
    return UPDATE_CHARACTERS


async def update_tags_skip(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Введите новых персонажей (через запятую, или нажмите /skip, чтобы оставить старых):")
    return UPDATE_CHARACTERS


async def update_characters(update: Update, context: CallbackContext) -> int:
    if update.message.text != "/skip":
        context.user_data['new_characters'] = [character.strip() for character in update.message.text.split(',')]
    handlers.update_image(
        context.user_data['id'],
        authors=context.user_data.get('new_authors'),
        tags=context.user_data.get('new_tags'),
        characters=context.user_data.get('new_characters')
    )
    await update.message.reply_text("✅ Запись обновлена!", parse_mode="HTML")
    return ConversationHandler.END


async def update_characters_skip(update: Update, context: CallbackContext) -> int:
    handlers.update_image(
        context.user_data['id'],
        authors=context.user_data.get('new_authors'),
        tags=context.user_data.get('new_tags'),
        characters=context.user_data.get('new_characters')
    )
    await update.message.reply_text("✅ Запись обновлена!", parse_mode="HTML")
    return ConversationHandler.END


# Команда /search_author
async def search_author(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🔍 Введите автора для поиска:")
    return "search_author"


async def search_author_result(update: Update, context: CallbackContext) -> None:
    author = update.message.text
    results = handlers.search_images_by_author(author)
    if results:
        for image in results:
            caption = (
                f"<b>ID:</b> {image.id}\n"
                f"<b>👤 Авторы:</b> {', '.join(a.name for a in image.authors)}\n"
                f"<b>🏷️ Теги:</b> {', '.join(t.name for t in image.tags)}\n"
                f"<b>👥 Персонажи:</b> {', '.join(c.name for c in image.characters)}"
            )
            try:
                await update.message.reply_photo(photo=open(image.file_path, 'rb'), caption=caption,
                                                 parse_mode="HTML")
            except FileNotFoundError:
                await update.message.reply_text(f"❌ Фотография с ID {image.id} не найдена на сервере.")
    else:
        await update.message.reply_text(f"❌ Записей с автором '{author}' не найдено.")


async def search_author_list(update: Update, context: CallbackContext) -> None:
    authors = handlers.get_all_authors()
    if not authors:
        await update.message.reply_text("❌ В базе данных нет авторов.")
        return

    context.user_data['author_index'] = 0
    context.user_data['authors'] = authors
    author = authors[0]
    await update.message.reply_text(
        f"<b>Автор:</b> {author.name}",
        parse_mode="HTML",
        reply_markup=create_author_navigation_buttons(0, len(authors))
    )


# Команда /search_tag
async def search_tag(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🔍 Введите тег для поиска:")
    return "search_tag"


async def search_tag_result(update: Update, context: CallbackContext) -> None:
    tag = update.message.text
    results = handlers.search_images_by_tag(tag)
    if results:
        for image in results:
            caption = (
                f"<b>ID:</b> {image.id}\n"
                f"<b>👤 Авторы:</b> {', '.join(a.name for a in image.authors)}\n"
                f"<b>🏷️ Теги:</b> {', '.join(t.name for t in image.tags)}\n"
                f"<b>👥 Персонажи:</b> {', '.join(c.name for c in image.characters)}"
            )
            try:
                await update.message.reply_photo(photo=open(image.file_path, 'rb'), caption=caption,
                                                 parse_mode="HTML")
            except FileNotFoundError:
                await update.message.reply_text(f"❌ Фотография с ID {image.id} не найдена на сервере.")
    else:
        await update.message.reply_text(f"❌ Записей с тегом '{tag}' не найдено.")


# Команда /search_character
async def search_character(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🔍 Введите персонажа для поиска:")
    return "search_character"


async def search_character_result(update: Update, context: CallbackContext) -> None:
    character = update.message.text
    results = handlers.search_images_by_character(character)
    if results:
        for image in results:
            caption = (
                f"<b>ID:</b> {image.id}\n"
                f"<b>👤 Авторы:</b> {', '.join(a.name for a in image.authors)}\n"
                f"<b>🏷️ Теги:</b> {', '.join(t.name for t in image.tags)}\n"
                f"<b>👥 Персонажи:</b> {', '.join(c.name for c in image.characters)}"
            )
            try:
                await update.message.reply_photo(photo=open(image.file_path, 'rb'), caption=caption,
                                                 parse_mode="HTML")
            except FileNotFoundError:
                await update.message.reply_text(f"❌ Фотография с ID {image.id} не найдена на сервере.")
    else:
        await update.message.reply_text(f"❌ Записей с персонажем '{character}' не найдено.")

async def tag_add_cmd(update: Update, context: CallbackContext) -> None:
    """Добавить теги к существующей записи."""
    if len(context.args) < 2:
        await update.message.reply_text("Использование: /tag_add <id> <tag1,tag2>")
        return
    try:
        image_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID должен быть числом.")
        return
    tags = [t.strip() for t in ' '.join(context.args[1:]).split(',') if t.strip()]
    handlers.add_tags(image_id, tags)
    await update.message.reply_text("✅ Теги добавлены.")


async def tag_remove_cmd(update: Update, context: CallbackContext) -> None:
    """Удалить тег из записи."""
    if len(context.args) < 2:
        await update.message.reply_text("Использование: /tag_remove <id> <tag>")
        return
    try:
        image_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID должен быть числом.")
        return
    tag = ' '.join(context.args[1:]).strip()
    if not tag:
        await update.message.reply_text("Укажите тег для удаления.")
        return
    handlers.remove_tag(image_id, tag)
    await update.message.reply_text("✅ Тег удалён.")

# Команда /display
async def display_entries(update: Update, context: CallbackContext) -> None:
    entries = handlers.get_all_images()
    if not entries:
        await update.message.reply_text("❌ В базе данных нет записей.")
        return

    image = entries[0]
    caption = (
        f"<b>ID:</b> {image.id}\n"
        f"<b>👤 Авторы:</b> {', '.join(a.name for a in image.authors)}\n"
        f"<b>🏷️ Теги:</b> {', '.join(t.name for t in image.tags)}\n"
        f"<b>👥 Персонажи:</b> {', '.join(c.name for c in image.characters)}"
    )
    try:
        context.user_data['current_index'] = 0
        context.user_data['display_entries'] = entries
        await update.message.reply_photo(
            photo=open(image.file_path, 'rb'),
            caption=caption,
            parse_mode="HTML",
            reply_markup=create_navigation_buttons(0, len(entries))
        )
    except FileNotFoundError:
        await update.message.reply_text(f"❌ Фотография с ID {image.id} не найдена на сервере.")
    except Exception as e:
        await update.message.reply_text(f"❌ Произошла ошибка при отображении фотографии: {str(e)}")


# Обработчик кнопок пролистывания
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Подтверждаем получение callback

    entries = context.user_data.get('display_entries', [])
    if not entries:
        await query.message.edit_text("❌ Ошибка: список записей недоступен.")
        return

    current_index = context.user_data.get('current_index', 0)
    callback_data = query.data

    # Определяем новый индекс
    try:
        if callback_data.startswith("prev_"):
            current_index = max(0, current_index - 1)
        elif callback_data.startswith("next_"):
            current_index = min(len(entries) - 1, current_index + 1)
    except ValueError:
        await query.message.edit_text("❌ Ошибка: неверные данные кнопки.")
        return

    context.user_data['current_index'] = current_index
    image = entries[current_index]

    caption = (
        f"<b>ID:</b> {image.id}\n"
        f"<b>👤 Авторы:</b> {', '.join(a.name for a in image.authors)}\n"
        f"<b>🏷️ Теги:</b> {', '.join(t.name for t in image.tags)}\n"
        f"<b>👥 Персонажи:</b> {', '.join(c.name for c in image.characters)}"
    )

    try:
        # Обновляем сообщение с новым фото и кнопками
        await query.message.edit_media(
            media=InputMediaPhoto(open(image.file_path, 'rb'), caption=caption, parse_mode="HTML"),
            reply_markup=create_navigation_buttons(current_index, len(entries))
        )
    except FileNotFoundError:
        await query.message.edit_text(f"❌ Фотография с ID {image.id} не найдена на сервере.")
    except Exception as e:
        await query.message.edit_text(f"❌ Произошла ошибка при обновлении фотографии: {str(e)}")


async def author_button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    authors = context.user_data.get('authors', [])
    if not authors:
        await query.message.edit_text("❌ Ошибка: список авторов недоступен.")
        return

    current_index = context.user_data.get('author_index', 0)
    data = query.data
    if data.startswith("author_prev_"):
        current_index = max(0, current_index - 1)
    elif data.startswith("author_next_"):
        current_index = min(len(authors) - 1, current_index + 1)

    context.user_data['author_index'] = current_index
    author = authors[current_index]
    await query.message.edit_text(
        f"<b>Автор:</b> {author.name}",
        parse_mode="HTML",
        reply_markup=create_author_navigation_buttons(current_index, len(authors))
    )


# Команда /cancel
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Операция отменена.",
        reply_markup=create_command_menu()
    )
    return ConversationHandler.END


# Команда /help
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "🌟 <b>Доступные команды:</b>\n\n"
        "/add - Добавить новую фотографию\n"
        "/update - Обновить запись\n"
        "/search_author - Найти по автору\n"
        "/search_tag - Найти по тегу\n"
        "/search_character - Найти по персонажу\n"
        "/tag_add - Добавить теги к записи\n"
        "/tag_remove - Удалить тег из записи\n"
        "/search_author_list - Список всех авторов\n"
        "/display - Показать все записи\n"
        "/help - Показать список команд",
        parse_mode="HTML",
        reply_markup=create_command_menu()
    )


def register_handlers(application: Application) -> None:
    """Зарегистрировать обработчики команд в приложении Telegram."""
    application.add_handler(CommandHandler("start", start))

    add_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_entry)],
        states={
            ADD_PHOTO: [MessageHandler(filters.PHOTO, add_photo)],
            ADD_AUTHORS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_authors)],
            ADD_TAGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_tags)],
            ADD_CHARACTERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_characters)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(add_conversation_handler)

    update_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('update', update_entry)],
        states={
            UPDATE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_id)],
            UPDATE_AUTHORS: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_authors),
                             CommandHandler('skip', update_authors_skip)],
            UPDATE_TAGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_tags),
                          CommandHandler('skip', update_tags_skip)],
            UPDATE_CHARACTERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_characters),
                                CommandHandler('skip', update_characters_skip)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(update_conversation_handler)

    search_author_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('search_author', search_author)],
        states={
            "search_author": [MessageHandler(filters.TEXT & ~filters.COMMAND, search_author_result)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(search_author_conversation_handler)

    search_tag_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('search_tag', search_tag)],
        states={
            "search_tag": [MessageHandler(filters.TEXT & ~filters.COMMAND, search_tag_result)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(search_tag_conversation_handler)

    search_character_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('search_character', search_character)],
        states={
            "search_character": [MessageHandler(filters.TEXT & ~filters.COMMAND, search_character_result)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(search_character_conversation_handler)

    application.add_handler(CommandHandler("tag_add", tag_add_cmd))
    application.add_handler(CommandHandler("tag_remove", tag_remove_cmd))
    application.add_handler(CommandHandler("display", display_entries))
    application.add_handler(CommandHandler("search_author_list", search_author_list))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^(prev|next)_"))
    application.add_handler(CallbackQueryHandler(author_button_handler, pattern="^(author_prev|author_next)_"))
    application.add_handler(CommandHandler("help", help_command))

