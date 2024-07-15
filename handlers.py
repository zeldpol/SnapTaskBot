import logging
from telegram import Update
from telegram.ext import CallbackContext

from admin import handle_admin_command, handle_poll_answer
from utils import load_channel_data, save_channel_data, load_themes

logger = logging.getLogger(__name__)

channel_data = load_channel_data()

def startbot(update: Update, context: CallbackContext):
    chat_id = str(update.channel_post.chat.id)
    if chat_id not in channel_data:
        channel_data[chat_id] = {
            "admins": set(),
            "themes": load_themes(),
            "current_theme": None
        }
        save_channel_data(channel_data)
        context.bot.send_message(chat_id=chat_id, text="Бот успешно активирован в этом канале!")
    else:
        context.bot.send_message(chat_id=chat_id, text="Бот уже активирован в этом канале.")

def deactivatebot(update: Update, context: CallbackContext):
    chat_id = str(update.channel_post.chat.id)
    if chat_id in channel_data:
        del channel_data[chat_id]
        save_channel_data(channel_data)
        context.bot.send_message(chat_id=chat_id, text="Бот деактивирован в этом канале.")
    else:
        context.bot.send_message(chat_id=chat_id, text="Бот не активирован в этом канале.")

def theme(update: Update, context: CallbackContext):
    chat_id = str(update.channel_post.chat.id)
    if chat_id in channel_data and channel_data[chat_id]["current_theme"]:
        current_theme = channel_data[chat_id]["current_theme"]
        context.bot.send_message(chat_id=chat_id, text=f"Текущая тема недели: {current_theme}")
    else:
        context.bot.send_message(chat_id=chat_id, text="Тема недели еще не установлена. Свяжитесь с администратором канала для установки темы.")

def handle_channel_post(update: Update, context: CallbackContext):
    if update.channel_post and update.channel_post.text:
        logger.info(f"Received message: {update.channel_post.text} in chat {update.channel_post.chat.id}")
        text = update.channel_post.text.lower()
        if '@snaptaskbot' in text:
            if 'startbot' in text:
                startbot(update, context)
            elif 'deactivatebot' in text:
                deactivatebot(update, context)
            elif 'theme' in text:
                theme(update, context)
    else:
        logger.info("Received a non-text message or update does not contain a message.")

def handle_private_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text
    logger.info(f"Received private message: {text} from user: {user_id}")
    handle_admin_command(user_id, text, context)

def handle_poll(update: Update, context: CallbackContext):
    handle_poll_answer(update, context)

def error_handler(update, context):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
