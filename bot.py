import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from handlers.admin_handler import handle_admin_command
from handlers.channel_handler import handle_channel_post, handle_poll_answer
from handlers.error_handler import error_handler
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def handle_private_message(update: Update, context: CallbackContext):
    handle_admin_command(update, context)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & Filters.private, handle_private_message))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.chat_type.channel, handle_channel_post))
    dispatcher.add_handler(MessageHandler(Filters.poll, handle_poll_answer))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
