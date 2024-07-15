import os
import json
import logging
from dotenv import load_dotenv
from telegram.ext import CallbackContext
from utils import load_default_themes, load_channel_data, save_channel_data

# Загрузка переменных окружения
load_dotenv()

logger = logging.getLogger(__name__)

ADMIN_PHRASE = os.getenv('ADMIN_PHRASE')
channel_data = load_channel_data()
default_themes = load_default_themes()

logger.info(f"ADMIN_PHRASE loaded: {ADMIN_PHRASE}")

def handle_admin_command(user_id, text, context: CallbackContext):
    logger.info(f"Received admin command: {text} from user: {user_id}")

    if text.startswith(f"authorize {ADMIN_PHRASE} "):
        try:
            _, _, channel_id = text.split()
            logger.info(f"Authorizing user {user_id} for channel {channel_id}")
            if channel_id not in channel_data:
                channel_data[channel_id] = {"admins": set(), "themes": default_themes.copy()}
            channel_data[channel_id]["admins"].add(user_id)
            save_channel_data(channel_data)
            context.bot.send_message(chat_id=user_id, text=f"Вы успешно авторизованы как администратор канала {channel_id}.")
        except ValueError:
            logger.error("Error parsing authorize command")
            context.bot.send_message(chat_id=user_id, text="Неверный формат команды. Используйте: authorize <кодовая фраза> <channel_id>")
    else:
        # Найти канал, в котором пользователь является администратором
        admin_channels = [chan for chan, data in channel_data.items() if user_id in data.get("admins", set())]

        if not admin_channels:
            context.bot.send_message(chat_id=user_id, text="Вы не авторизованы ни в одном канале. Отправьте команду в формате: authorize <кодовая фраза> <channel_id> для авторизации.")
            return

        if text.startswith("addtheme "):
            new_theme = text.split(" ", 1)[1]
            for channel_id in admin_channels:
                channel_data[channel_id]["themes"].append(new_theme)
            save_channel_data(channel_data)
            context.bot.send_message(chat_id=user_id, text=f"Тема '{new_theme}' успешно добавлена в список тем для каналов {', '.join(admin_channels)}.")
        else:
            context.bot.send_message(chat_id=user_id, text="Неизвестная команда. Доступные команды: addtheme <тема>")
