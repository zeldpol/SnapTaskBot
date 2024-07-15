import random
from telegram.ext import CallbackContext
from admin.utils import get_admin_channel, save_channel_data, channel_data

def new_theme(user_id, args, context: CallbackContext):
    if len(args) != 0:
        context.bot.send_message(chat_id=user_id, text="Используйте: newtheme")
        return
    channel_id = get_admin_channel(user_id)
    if channel_id:
        themes = channel_data[channel_id].get("themes", [])
        if themes:
            selected_theme = random.choice(themes)
            channel_data[channel_id]["current_theme"] = selected_theme
            save_channel_data(channel_data)
            context.bot.send_message(chat_id=channel_id, text=f"Новая тема недели: {selected_theme}")
        else:
            context.bot.send_message(chat_id=channel_id, text="В канале нет доступных тем.")
    else:
        context.bot.send_message(chat_id=user_id, text="Вы не авторизованы ни в одном канале.")
