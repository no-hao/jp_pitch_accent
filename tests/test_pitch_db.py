import unittest
import os
from pitch_db import PitchDB

class TestPitchDB(unittest.TestCase):
    def setUp(self):
        self.db = PitchDB()

    def test_lookup_known_word(self):
        result = self.db.lookup("食べる")
        self.assertIsNotNone(result)
        self.assertEqual(result["reading"], "たべる")
        self.assertEqual(result["pitch"], 1)

    def test_lookup_unknown_word(self):
        result = self.db.lookup("未知語")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
