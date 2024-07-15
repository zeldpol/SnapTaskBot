import json
import os

DATA_DIR = "data"
CHANNEL_DATA_FILE = os.path.join(DATA_DIR, "channel_data.json")

def load_channel_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    try:
        with open(CHANNEL_DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Преобразуем admins обратно в set
            for key in data:
                if isinstance(data[key].get("admins"), list):
                    data[key]["admins"] = set(data[key]["admins"])
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_channel_data(data):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for key in data:
        if isinstance(data[key].get("admins"), set):
            data[key]["admins"] = list(data[key]["admins"])  # Преобразование set в список перед сериализацией
    with open(CHANNEL_DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
import json
import os

DATA_DIR = "data"
CHANNEL_DATA_FILE = os.path.join(DATA_DIR, "channel_data.json")

def load_channel_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    try:
        with open(CHANNEL_DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Преобразуем admins обратно в set
            for key in data:
                if isinstance(data[key].get("admins"), list):
                    data[key]["admins"] = set(data[key]["admins"])
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_channel_data(data):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for key in data:
        if isinstance(data[key].get("admins"), set):
            data[key]["admins"] = list(data[key]["admins"])  # Преобразование set в список перед сериализацией
    with open(CHANNEL_DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
