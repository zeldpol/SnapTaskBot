import random
from telegram.ext import CallbackContext
from admin.utils import get_admin_channel, save_channel_data, channel_data

min_themes = 4

def start_vote(user_id, args, context: CallbackContext):
    if len(args) != 0:
        context.bot.send_message(chat_id=user_id, text="Используйте: startvote")
        return
    channel_id = get_admin_channel(user_id)
    if channel_id:
        if "active_poll" in channel_data[channel_id]:
            context.bot.send_message(chat_id=user_id, text=f"В канале {channel_id} уже идет голосование.")
            return
        themes = channel_data[channel_id].get("themes", [])
        if len(themes) < 2:
            context.bot.send_message(chat_id=user_id, text=f"Недостаточно тем для голосования в канале {channel_id}.")
            return
        elif len(themes) > 2 and len(themes) < min_themes:
            options = random.sample(themes, len(themes))
        else:
            options = random.sample(themes, min_themes)
        message = context.bot.send_poll(
            chat_id=channel_id,
            question="Голосование за тему недели:",
            options=options,
            is_anonymous=True,
            allows_multiple_answers=False
        )
        channel_data[channel_id]["active_poll"] = {
            "poll_id": message.poll.id,
            "message_id": message.message_id,
            "options": options
        }
        save_channel_data(channel_data)
    else:
        context.bot.send_message(chat_id=user_id, text="Вы не авторизованы ни в одном канале.")