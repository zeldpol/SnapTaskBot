import logging
from telegram.ext import CallbackContext
from admin.utils import get_admin_channel, save_channel_data, channel_data

logger = logging.getLogger(__name__)

def end_vote(user_id, args, context: CallbackContext):
    if len(args) != 0:
        context.bot.send_message(chat_id=user_id, text="Используйте: endvote")
        return
    channel_id = get_admin_channel(user_id)
    if channel_id:
        active_poll = channel_data[channel_id].get("active_poll")
        if not active_poll:
            context.bot.send_message(chat_id=user_id, text=f"Голосование в канале {channel_id} не проводилось.")
            return
        message_id = active_poll["message_id"]

        # Получение результатов опроса через API Telegram
        try:
            # Закрытие опроса
            poll = context.bot.stop_poll(chat_id=channel_id, message_id=message_id)
            poll_results = {option['text']: option['voter_count'] for option in poll['options']}
            most_voted_option = max(poll_results, key=poll_results.get)

            channel_data[channel_id]["current_theme"] = most_voted_option
            del channel_data[channel_id]["active_poll"]
            save_channel_data(channel_data)
            context.bot.send_message(chat_id=user_id, text=f"Итоги голосования подведены. Тема недели '{most_voted_option}' установлена для канала {channel_id}.")
            context.bot.send_message(chat_id=channel_id, text=f"Итоги голосования подведены. Тема недели: {most_voted_option}")
        except Exception as e:
            logger.error(f"Ошибка при получении результатов опроса: {e}")
            context.bot.send_message(chat_id=user_id, text=f"Не удалось получить данные голосования для канала {channel_id}.")
    else:
        context.bot.send_message(chat_id=user_id, text="Вы не авторизованы ни в одном канале.")
