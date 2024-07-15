import logging
import os
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters

from handlers import handle_channel_post, handle_private_message, error_handler

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_PHRASE = os.getenv('ADMIN_PHRASE')

# Проверка загрузки переменных окружения
if not TOKEN:
    logger.error("TELEGRAM_TOKEN not found in environment variables.")
if not ADMIN_PHRASE:
    logger.error("ADMIN_PHRASE not found in environment variables.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчик для всех текстовых сообщений в канале
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.chat_type.channel, handle_channel_post))

    # Обработчик для личных сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.chat_type.private, handle_private_message))

    # Регистрация обработчика ошибок
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
