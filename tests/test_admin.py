# tests/test_admin.py
import unittest
from unittest.mock import Mock
from admin import handle_admin_command
from utils import load_channel_data, save_channel_data

class TestAdminCommands(unittest.TestCase):
    def setUp(self):
        self.user_id = 12345
        self.channel_id = '-1001234567890'
        self.context = Mock()
        self.channel_data = load_channel_data()
        self.channel_data[self.channel_id] = {"admins": set(), "themes": []}
        save_channel_data(self.channel_data)

    def test_authorize_command(self):
        command = f"authorize thereisnospoon {self.channel_id}"
        handle_admin_command(self.user_id, command, self.context)
        self.channel_data = load_channel_data()
        self.assertIn(self.user_id, self.channel_data[self.channel_id]['admins'])

    def test_addtheme_command(self):
        # Авторизация пользователя
        command = f"authorize thereisnospoon {self.channel_id}"
        handle_admin_command(self.user_id, command, self.context)

        # Добавление новой темы
        new_theme = "Новая тема"
        command = f"addtheme {new_theme}"
        handle_admin_command(self.user_id, command, self.context)

        self.channel_data = load_channel_data()
        self.assertIn(new_theme, self.channel_data[self.channel_id]['themes'])

if __name__ == '__main__':
    unittest.main()
