from telegram.ext import CallbackContext
from admin.utils import get_admin_channel, channel_data

def show_theme(user_id, args, context: CallbackContext):
    if len(args) != 0:
        context.bot.send_message(chat_id=user_id, text="Используйте: showtheme")
        return
    channel_id = get_admin_channel(user_id)
    if channel_id:
        current_theme = channel_data[channel_id].get("current_theme")
        if current_theme:
            context.bot.send_message(chat_id=channel_id, text=f"Текущая тема недели: {current_theme}")
        else:
            context.bot.send_message(chat_id=channel_id, text="Тема недели еще не установлена.")
    else:
        context.bot.send_message(chat_id=user_id, text="Вы не авторизованы ни в одном канале.")
