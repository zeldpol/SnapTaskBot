import os
import json
import logging
from dotenv import load_dotenv
from telegram.ext import CallbackContext
from utils import load_default_themes, load_admin_users, save_admin_users

# Загрузка переменных окружения
load_dotenv()

logger = logging.getLogger(__name__)

ADMIN_PHRASE = os.getenv('ADMIN_PHRASE')
admin_users = load_admin_users()
default_themes = load_default_themes()

def handle_admin_command(user_id, text, context: CallbackContext):
    logger.info(f"Received admin command: {text} from user: {user_id}")
    
    if text == ADMIN_PHRASE:
        admin_users.add(user_id)
        save_admin_users(admin_users)
        context.bot.send_message(chat_id=user_id, text="Вы успешно авторизованы как администратор.")
    elif user_id in admin_users:
        if text.startswith("addtheme "):
            new_theme = text.split(" ", 1)[1]
            default_themes.append(new_theme)
            with open('themes.json', 'w', encoding='utf-8') as file:
                json.dump(default_themes, file, ensure_ascii=False, indent=4)
            context.bot.send_message(chat_id=user_id, text=f"Тема '{new_theme}' успешно добавлена в список по умолчанию.")
        else:
            context.bot.send_message(chat_id=user_id, text="Неизвестная команда. Доступные команды: addtheme <тема>")
    else:
        context.bot.send_message(chat_id=user_id, text="Вы не авторизованы. Отправьте секретную фразу для авторизации.")
