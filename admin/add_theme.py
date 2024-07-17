from telegram.ext import CallbackContext
from admin.utils import get_admin_channel, save_channel_data, channel_data

def add_theme(user_id, args, context: CallbackContext):
    if len(args) < 1:
        context.bot.send_message(chat_id=user_id, text="Используйте: addtheme <тема>")
        return
    new_theme = ' '.join(args)  # Объединяем аргументы в одну строку
    channel_id = get_admin_channel(user_id)
    if channel_id:
        channel_data[channel_id]["themes"].append(new_theme)
        save_channel_data(channel_data)
        context.bot.send_message(chat_id=user_id, text=f"Тема '{new_theme}' успешно добавлена в список тем для канала {channel_id}.")
    else:
        context.bot.send_message(chat_id=user_id, text="Вы не авторизованы ни в одном канале.")
