import json
import logging

logger = logging.getLogger(__name__)

def load_json_file(file_path, default_value=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read().strip()
            if not data:  # Check if the file is empty
                logger.warning(f"File {file_path} is empty. Returning default value.")
                return default_value
            return json.loads(data)
    except FileNotFoundError:
        logger.warning(f"File {file_path} not found. Returning default value.")
        return default_value
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from file {file_path}. Returning default value.")
        return default_value

def load_channel_data():
    data = load_json_file('channel_data.json', default_value={})
    for channel_id, channel_info in data.items():
        if 'admins' not in channel_info:
            channel_info['admins'] = set()
        else:
            channel_info['admins'] = set(channel_info['admins'])
    return data

def save_channel_data(channel_data):
    data = {chan_id: {'admins': list(info['admins']), 'themes': info['themes'], 'current_theme': info.get('current_theme'), 'voting_options': info.get('voting_options', []), 'voting_results': info.get('voting_results', {})} for chan_id, info in channel_data.items()}
    with open('channel_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_themes():
    return load_json_file('themes.json', default_value=[])
