from telegram.ext import CallbackContext
from admin.utils import get_admin_channel, channel_data

def list_themes(user_id, args, context: CallbackContext):
    if len(args) != 0:
        context.bot.send_message(chat_id=user_id, text="Используйте: themes")
        return
    channel_id = get_admin_channel(user_id)
    if channel_id:
        themes = channel_data[channel_id].get("themes", [])
        if themes:
            context.bot.send_message(chat_id=user_id, text=f"Темы в канале {channel_id}:\n" + "\n".join(themes))
        else:
            context.bot.send_message(chat_id=user_id, text=f"В канале {channel_id} нет доступных тем.")
    else:
        context.bot.send_message(chat_id=user_id, text="Вы не авторизованы ни в одном канале.")
