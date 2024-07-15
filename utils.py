import json

def load_channel_data():
    try:
        with open('channel_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for channel_id, channel_info in data.items():
                if 'admins' not in channel_info:
                    channel_info['admins'] = set()
                else:
                    channel_info['admins'] = set(channel_info['admins'])
            return data
    except FileNotFoundError:
        return {}

def save_channel_data(channel_data):
    data = {chan_id: {'admins': list(info['admins']), 'themes': info['themes']} for chan_id, info in channel_data.items()}
    with open('channel_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

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
