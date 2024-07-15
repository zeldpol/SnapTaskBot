# tests/test_handlers.py
import unittest
from unittest.mock import Mock, MagicMock
from telegram import Update, Message, Chat
from handlers import startbot, deactivatebot, theme, handle_channel_post
from utils import load_channel_data, save_channel_data

class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.context = Mock()
        self.update = Mock(spec=Update)
        self.channel_id = '-1001234567890'
        self.chat = Mock(spec=Chat)
        self.chat.id = self.channel_id
        self.update.channel_post.chat = self.chat
        self.update.channel_post.text = ''
        self.channel_data = load_channel_data()

    def test_startbot(self):
        startbot(self.update, self.context)
        self.assertIn(self.channel_id, self.channel_data)

    def test_deactivatebot(self):
        startbot(self.update, self.context)
        deactivatebot(self.update, self.context)
        self.assertNotIn(self.channel_id, self.channel_data)

    def test_theme(self):
        startbot(self.update, self.context)
        self.channel_data[self.channel_id]['themes'] = ["Test Theme"]
        save_channel_data(self.channel_data)
        
        self.update.channel_post.text = '@snaptaskbot theme'
        handle_channel_post(self.update, self.context)
        
        self.channel_data = load_channel_data()
        self.assertNotIn("Test Theme", self.channel_data[self.channel_id]['themes'])

if __name__ == '__main__':
    unittest.main()
