import logging
from telegram import Update
from telegram.ext import CallbackContext
from admin.authorize_admin import authorize_admin
from admin.add_theme import add_theme
from admin.start_vote import start_vote
from admin.end_vote import end_vote
from admin.show_theme import show_theme
from admin.new_theme import new_theme
from admin.list_themes import list_themes

logger = logging.getLogger(__name__)

def handle_admin_command(user_id, text, context: CallbackContext):
    logger.info(f"Received admin command: {text} from user: {user_id}")

    command, *args = text.split(maxsplit=1)
    args = args[0].split() if args else []
    command_func = {
        "authorize": authorize_admin,
        "addtheme": add_theme,
        "startvote": start_vote,
        "endvote": end_vote,
        "showtheme": show_theme,
        "newtheme": new_theme,
        "themes": list_themes,
    }.get(command.lower())

    if command_func:
        command_func(user_id, args, context)
    else:
        context.bot.send_message(chat_id=user_id, text="Неизвестная команда. Доступные команды: authorize, addtheme, startvote, endvote, showtheme, newtheme, themes")
