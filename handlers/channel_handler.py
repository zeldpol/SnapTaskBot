import logging
from telegram import Update
from telegram.ext import CallbackContext
from utils.channel_data import load_channel_data, save_channel_data
from utils.themes import load_themes

logger = logging.getLogger(__name__)

channel_data = load_channel_data()

def startbot(update: Update, context: CallbackContext):
    chat_id = str(update.channel_post.chat.id)
    if chat_id not in channel_data:
        channel_data[chat_id] = {
            "admins": set(),  # Используем set для администраторов
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

def handle_channel_post(update: Update, context: CallbackContext):
    if update.channel_post and update.channel_post.text:
        logger.info(f"Received message: {update.channel_post.text} in chat {update.channel_post.chat.id}")
        text = update.channel_post.text.lower()
        if '@snaptaskbot' in text:
            if 'startbot' in text:
                logger.info("Handling startbot command in channel.")
                startbot(update, context)
            elif 'deactivatebot' in text:
                logger.info("Handling deactivatebot command in channel.")
                deactivatebot(update, context)
    else:
        logger.info("Received a non-text message or update does not contain a message.")

def handle_poll_answer(update: Update, context: CallbackContext):
    answer = update.poll_answer
    poll_id = answer.poll_id
    option_ids = answer.option_ids
    for channel_id, data in channel_data.items():
        active_poll = data.get("active_poll")
        if active_poll and active_poll["poll_id"] == poll_id:
            selected_options = [active_poll["options"][i] for i in option_ids]
            for option in selected_options:
                if poll_id not in context.bot_data:
                    context.bot_data[poll_id] = {
                        "voting_results": {opt: 0 for opt in active_poll["options"]}
                    }
                context.bot_data[poll_id]["voting_results"][option] += 1
            save_channel_data(channel_data)
            break
