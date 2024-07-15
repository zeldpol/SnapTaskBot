import os
import logging
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext
from utils import load_themes, load_channel_data, save_channel_data

# Загрузка переменных окружения
load_dotenv()

logger = logging.getLogger(__name__)

ADMIN_PHRASE = os.getenv('ADMIN_PHRASE')
channel_data = load_channel_data()
themes = load_themes()

logger.info(f"ADMIN_PHRASE loaded: {ADMIN_PHRASE}")

def authorize_admin(user_id, channel_id, context: CallbackContext):
    if channel_id in channel_data:
        channel_data[channel_id]["admins"].add(user_id)
        save_channel_data(channel_data)
        context.bot.send_message(chat_id=user_id, text=f"Вы успешно авторизованы как администратор канала {channel_id}.")
    else:
        context.bot.send_message(chat_id=user_id, text=f"Канал с ID {channel_id} не найден. Пожалуйста, сначала активируйте бот в канале с помощью команды startbot.")

def handle_admin_command(user_id, text, context: CallbackContext):
    logger.info(f"Received admin command: {text} from user: {user_id}")

    if text.startswith(f"authorize {ADMIN_PHRASE} "):
        try:
            _, _, channel_id = text.split()
            authorize_admin(user_id, channel_id, context)
        except ValueError:
            context.bot.send_message(chat_id=user_id, text="Неверный формат команды. Используйте: authorize <кодовая фраза> <channel_id>")
        return

    admin_channels = [chan for chan, data in channel_data.items() if user_id in data.get("admins", set())]
    if not admin_channels:
        context.bot.send_message(chat_id=user_id, text="Вы не авторизованы ни в одном канале. Отправьте команду в формате: authorize <кодовая фраза> <channel_id> для авторизации.")
        return

    command, *args = text.split(maxsplit=1)
    command_func = {
        "addtheme": add_theme,
        "settheme": set_theme,
        "pickthemes": pick_themes,
        "startvote": start_vote,
        "finalizevote": finalize_vote,
    }.get(command.lower())

    if command_func:
        command_func(user_id, args, context, admin_channels)
    else:
        context.bot.send_message(chat_id=user_id, text="Неизвестная команда. Доступные команды: addtheme <тема>, settheme <channel_id> <тема>, pickthemes <channel_id>, startvote <channel_id>, finalizevote <channel_id>")

def add_theme(user_id, args, context, admin_channels):
    new_theme = args[0] if args else None
    if new_theme:
        for channel_id in admin_channels:
            channel_data[channel_id]["themes"].append(new_theme)
        save_channel_data(channel_data)
        context.bot.send_message(chat_id=user_id, text=f"Тема '{new_theme}' успешно добавлена в список тем для каналов {', '.join(admin_channels)}.")
    else:
        context.bot.send_message(chat_id=user_id, text="Используйте: addtheme <тема>")

def set_theme(user_id, args, context, admin_channels):
    try:
        if len(args) == 1 and len(admin_channels) == 1:
            channel_id = admin_channels[0]
            theme = args[0]
        else:
            channel_id, theme = args[0].split(maxsplit=1)
        if channel_id in admin_channels and theme:
            channel_data[channel_id]["current_theme"] = theme
            save_channel_data(channel_data)
            context.bot.send_message(chat_id=user_id, text=f"Тема недели '{theme}' успешно установлена для канала {channel_id}.")
            context.bot.send_message(chat_id=channel_id, text=f"Новая тема недели: {theme}")
        else:
            raise ValueError
    except ValueError:
        context.bot.send_message(chat_id=user_id, text="Используйте: settheme <channel_id> <тема>")

def pick_themes(user_id, args, context, admin_channels):
    try:
        if len(args) == 1:
            channel_id = args[0]
        elif len(admin_channels) == 1:
            channel_id = admin_channels[0]
        else:
            raise ValueError
        if len(channel_data[channel_id]["themes"]) < 2:
            context.bot.send_message(chat_id=user_id, text=f"В канале {channel_id} недостаточно тем для выбора.")
        else:
            chosen_themes = random.sample(channel_data[channel_id]["themes"], min(4, len(channel_data[channel_id]["themes"])))
            channel_data[channel_id]["voting_options"] = chosen_themes
            save_channel_data(channel_data)
            context.bot.send_message(chat_id=user_id, text=f"Темы для голосования успешно выбраны для канала {channel_id}. Запустите голосование командой /startvote <channel_id>")
    except ValueError:
        context.bot.send_message(chat_id=user_id, text="Используйте: pickthemes <channel_id>")

def start_vote(user_id, args, context, admin_channels):
    try:
        if len(args) == 1:
            channel_id = args[0]
        elif len(admin_channels) == 1:
            channel_id = admin_channels[0]
        else:
            raise ValueError
        if "voting_options" in channel_data[channel_id]:
            options = channel_data[channel_id]["voting_options"]
            if len(options) < 2:
                context.bot.send_message(chat_id=user_id, text=f"Недостаточно вариантов для голосования. Необходимо минимум 2 варианта.")
                return
            message = context.bot.send_poll(
                chat_id=channel_id,
                question="Голосование за тему недели:",
                options=options,
                is_anonymous=True,  # Теперь анонимный опрос
                allows_multiple_answers=False
            )
            payload = {
                message.poll.id: {
                    "chat_id": channel_id,
                    "message_id": message.message_id,
                    "voting_options": options,
                    "voting_results": {theme: 0 for theme in options}
                }
            }
            context.bot_data.update(payload)
            save_channel_data(channel_data)
        else:
            context.bot.send_message(chat_id=user_id, text=f"Темы для голосования не выбраны. Пожалуйста, используйте команду pickthemes <channel_id>.")
    except ValueError:
        context.bot.send_message(chat_id=user_id, text="Используйте: startvote <channel_id>")

def finalize_vote(user_id, args, context, admin_channels):
    try:
        if len(args) == 1:
            channel_id = args[0]
        elif len(admin_channels) == 1:
            channel_id = admin_channels[0]
        else:
            raise ValueError
        poll_results = channel_data[channel_id].get("voting_results", {})
        if poll_results:
            most_voted_theme = max(poll_results, key=poll_results.get)
            channel_data[channel_id]["current_theme"] = most_voted_theme
            save_channel_data(channel_data)
            context.bot.send_message(chat_id=user_id, text=f"Итоги голосования подведены. Тема недели '{most_voted_theme}' установлена для канала {channel_id}.")
            context.bot.send_message(chat_id=channel_id, text=f"Итоги голосования подведены. Тема недели: {most_voted_theme}")
        else:
            context.bot.send_message(chat_id=user_id, text=f"Голосование в канале {channel_id} не проводилось.")
    except ValueError:
        context.bot.send_message(chat_id=user_id, text="Используйте: finalizevote <channel_id>")

def handle_poll_answer(update: Update, context: CallbackContext):
    answer = update.poll_answer
    poll_id = answer.poll_id
    option_ids = answer.option_ids
    poll_data = context.bot_data.get(poll_id)
    if poll_data:
        selected_options = [poll_data["voting_options"][i] for i in option_ids]
        for option in selected_options:
            poll_data["voting_results"][option] += 1
        channel_data[poll_data["chat_id"]]["voting_results"] = poll_data["voting_results"]
        save_channel_data(channel_data)
