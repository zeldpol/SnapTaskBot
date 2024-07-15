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
        if not themes:
            context.bot.send_message(chat_id=user_id, text=f"Нет доступных тем для канала {channel_id}.")
            return
        new_theme = random.choice(themes)
        
        # Удаление выбранной темы из списка доступных тем
        channel_data[channel_id]["themes"].remove(new_theme)
        
        channel_data[channel_id]["current_theme"] = new_theme
        save_channel_data(channel_data)
        context.bot.send_message(chat_id=user_id, text=f"Новая тема недели '{new_theme}' установлена для канала {channel_id}.")
        context.bot.send_message(chat_id=channel_id, text=f"Новая тема недели: {new_theme}")
    else:
        context.bot.send_message(chat_id=user_id, text="Вы не авторизованы ни в одном канале.")
