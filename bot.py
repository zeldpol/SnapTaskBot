import logging
from telegram.ext import Updater, MessageHandler, Filters, PollAnswerHandler
from dotenv import load_dotenv
import os
from handlers.admin_handler import handle_admin_command
from handlers.channel_handler import handle_channel_post, handle_poll_answer
from handlers.error_handler import error_handler
from utils.logging import setup_logging

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logger = setup_logging()

TOKEN = os.getenv('TELEGRAM_TOKEN')

def handle_private_message(update, context):
    user_id = update.effective_user.id if update.effective_user else None
    if not user_id:
        logger.error("Received private message without effective user.")
        return

    text = update.message.text
    logger.info(f"Received private message: {text} from user: {user_id}")
    handle_admin_command(user_id, text, context)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & Filters.chat_type.private, handle_private_message))
    dispatcher.add_handler(MessageHandler(Filters.chat_type.channel, handle_channel_post))
    dispatcher.add_handler(PollAnswerHandler(handle_poll_answer))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
