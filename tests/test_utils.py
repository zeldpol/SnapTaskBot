# tests/test_utils.py
import unittest
from utils import load_channel_data, save_channel_data, load_default_themes

class TestUtils(unittest.TestCase):
    def test_load_default_themes(self):
        themes = load_default_themes()
        self.assertIsInstance(themes, list)

    def test_load_and_save_channel_data(self):
        data = load_channel_data()
        self.assertIsInstance(data, dict)

        test_channel_id = '-1001234567890'
        data[test_channel_id] = {"admins": set(), "themes": []}
        save_channel_data(data)

        loaded_data = load_channel_data()
        self.assertIn(test_channel_id, loaded_data)

if __name__ == '__main__':
    unittest.main()
