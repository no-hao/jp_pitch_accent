import unittest
import os
from pitch_db import PitchDB
from unittest.mock import patch

class TestPitchDB(unittest.TestCase):
    def setUp(self):
        # Use a temporary copy of the DB for testing
        self.test_db_path = 'test_pitch_db.json'
        with open('pitch_db.json', encoding='utf-8') as f:
            data = f.read()
        with open(self.test_db_path, 'w', encoding='utf-8') as f:
            f.write(data)
        self.db = PitchDB(self.test_db_path)

    def tearDown(self):
        os.remove(self.test_db_path)

    def test_lookup_known_word(self):
        result = self.db.lookup("食べる")
        self.assertIsNotNone(result)
        self.assertEqual(result["reading"], "たべる")
        self.assertEqual(result["pitch"], 1)

    def test_lookup_unknown_word(self):
        result = self.db.lookup("未知語")
        self.assertIsNone(result)

    @patch.object(PitchDB, 'fetch_from_ojad')
    def test_lookup_with_cache_fetches_and_saves(self, mock_fetch):
        # Simulate OJAD returning reading and pitch for a new word
        mock_fetch.return_value = ("みちご", 3)
        result = self.db.lookup_with_cache("未知語")
        self.assertIsNotNone(result)
        self.assertEqual(result["reading"], "みちご")
        self.assertEqual(result["pitch"], 3)
        # Now it should be in the DB
        result2 = self.db.lookup("未知語")
        self.assertIsNotNone(result2)
        self.assertEqual(result2["reading"], "みちご")
        self.assertEqual(result2["pitch"], 3)

if __name__ == "__main__":
    unittest.main()
