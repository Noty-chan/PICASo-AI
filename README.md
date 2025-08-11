# 🖼️ Image TagBot - Telegram бот для организации изображений

**Умный бот для хранения и сортировки изображений по тегам, авторам и персонажам**

[![Python](https://img.shields.io/badge/Python-3.9+-yellow?logo=python)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram%20Bot-API%2020+-blue?logo=telegram)](https://core.telegram.org/bots/api)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## ✨ Возможности

- 📤 **Загрузка изображений** прямо в чат с ботом
- 🏷 **Гибкая система тегов**:
  - Добавление неограниченного количества тегов
  - Группировка по авторам, персонажам, жанрам
  - Пользовательские категории тегов
- 🔍 **Удобный поиск**:
  - Поиск по комбинации тегов
  - Фильтрация по авторам/персонажам
  - Быстрый доступ к недавним загрузкам
- 📁 **Организация коллекции**:
  - Альбомная система
  - Избранные подборки
  - Экспорт метаданных

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.9 или новее
- Аккаунт Telegram и токен бота (получить у [@BotFather](https://t.me/BotFather))
- База данных (SQLite/PostgreSQL)

### Установка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-username/image-tagbot.git
cd image-tagbot
```
2. Установите токен бота в переменную окружения `BOT_TOKEN`:
```bash
export BOT_TOKEN="ВАШ_ТОКЕН"
```
