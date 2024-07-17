import logging
from telegram import Update
from telegram.ext import CallbackContext
from admin.authorize_admin import authorize_admin
from admin.new_theme import new_theme
from admin.end_vote import end_vote
from admin.add_theme import add_theme
from admin.start_vote import start_vote
from admin.show_theme import show_theme

logger = logging.getLogger(__name__)

def handle_admin_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text
    args = text.split()[1:]
    command = text.split()[0].lower()
    
    command_map = {
        '/authorize': authorize_admin,
        '/newtheme': new_theme,
        '/endvote': end_vote,
        '/addtheme': add_theme,
        '/startvote': start_vote,
        '/showtheme': show_theme,
    }
    
    if command in command_map:
        logger.info(f"Executing command: {command} with args: {args} for user: {user_id}")
        command_map[command](user_id, args, context)
    else:
        context.bot.send_message(chat_id=user_id, text="Неизвестная команда. Доступные команды: authorize, newtheme, endvote, addtheme, startvote, showtheme.")
