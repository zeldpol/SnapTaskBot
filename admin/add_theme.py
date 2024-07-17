from telegram.ext import CallbackContext
from admin.utils import get_admin_channel, save_channel_data, load_channel_data

def add_theme(user_id, args, context: CallbackContext):
    if len(args) < 1:
        context.bot.send_message(chat_id=user_id, text="Используйте: addtheme <тема>")
        return
    theme = ' '.join(args)
    channel_id = get_admin_channel(user_id)
    if channel_id:
        channel_data = load_channel_data()
        if channel_id not in channel_data:
            context.bot.send_message(chat_id=user_id, text=f"Канал с ID {channel_id} не найден.")
            return
        if "themes" not in channel_data[channel_id]:
            channel_data[channel_id]["themes"] = []
        channel_data[channel_id]["themes"].append(theme)
        save_channel_data(channel_data)
        context.bot.send_message(chat_id=user_id, text=f"Тема '{theme}' добавлена в список доступных тем для канала {channel_id}.")
    else:
        context.bot.send_message(chat_id=user_id, text="Вы не авторизованы ни в одном канале.")
