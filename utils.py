import json

def load_channel_data():
    try:
        with open('channel_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_channel_data(channel_data):
    with open('channel_data.json', 'w', encoding='utf-8') as file:
        json.dump(channel_data, file, ensure_ascii=False, indent=4)

def load_default_themes():
    try:
        with open('themes.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return [
            "Силуэты в городском закате",
            "Спешащие люди",
            "Старинные двери и окна",
            "Уличные музыканты",
            "Дождь на городских улицах",
            "Отражения в лужах",
            "Кафе на тротуаре",
            "Цветы в городском асфальте",
            "Архитектурные линии и углы",
            "Жизнь в парке",
            "Скрытые уголки города",
            "Уличное искусство и граффити",
            "Портреты собак на прогулке",
            "Велосипеды в городе",
            "Люди и их мобильные телефоны",
            "Заброшенные здания",
            "Модные аксессуары прохожих",
            "Ночные огни и неон",
            "Раннее утро перед суетой",
            "Суета общественного транспорта"
        ]

def load_admin_users():
    try:
        with open('admin_users.json', 'r', encoding='utf-8') as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

def save_admin_users(admin_users):
    with open('admin_users.json', 'w', encoding='utf-8') as file:
        json.dump(list(admin_users), file, ensure_ascii=False, indent=4)
