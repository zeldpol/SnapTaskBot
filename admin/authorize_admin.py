import logging
from telegram.ext import CallbackContext
from admin.utils import save_channel_data, load_channel_data
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

load_dotenv()
SECRET_PHRASE = os.getenv('SECRET_PHRASE')

def authorize_admin(user_id, args, context: CallbackContext):
    if len(args) != 2:
        context.bot.send_message(chat_id=user_id, text="Используйте: authorize <секретная_фраза> <channel_id>")
        return
    secret_phrase, channel_id = args
    logger.info(f"Received secret phrase: {secret_phrase}, expected: {SECRET_PHRASE}")
    if secret_phrase != SECRET_PHRASE:
        context.bot.send_message(chat_id=user_id, text="Неправильная секретная фраза.")
        return

    # Повторная загрузка данных
    channel_data = load_channel_data()

    # Проверка, что пользователь не является администратором другого канала
    for cid, data in channel_data.items():
        if user_id in data["admins"]:
            context.bot.send_message(chat_id=user_id, text=f"Вы уже администратор канала {cid}. Один пользователь может быть администратором только одного канала.")
            return

    if channel_id in channel_data:
        logger.info(f"Authorizing user {user_id} as admin of channel {channel_id}.")
        channel_data[channel_id]["admins"].add(user_id)  # Используем метод add для set
        save_channel_data(channel_data)
        context.bot.send_message(chat_id=user_id, text=f"Вы успешно авторизованы как администратор канала {channel_id}.")
    else:
        logger.info(f"Channel {channel_id} not found in channel_data.")
        context.bot.send_message(chat_id=user_id, text=f"Канал с ID {channel_id} не найден. Пожалуйста, сначала активируйте бот в канале с помощью команды startbot.")
