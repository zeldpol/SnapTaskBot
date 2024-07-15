from utils.channel_data import load_channel_data, save_channel_data

channel_data = load_channel_data()

def get_admin_channel(user_id):
    for cid, data in channel_data.items():
        if user_id in data["admins"]:
            return cid
    return None
