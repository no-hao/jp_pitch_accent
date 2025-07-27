import unittest
import sys
import os
import requests
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pitch_db import PitchDB, PITCH_TYPE_LABELS

class TestOJAD(unittest.TestCase):
    """Test OJAD integration functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = PitchDB()
        
        # Chart-based test cases: (word, expected_drop_pos, expected_type_label)
        self.test_cases = [
            # Heiban (0)
            ("名", 0, "Heiban"),
            ("水", 0, "Heiban"),
            ("会社", 0, "Heiban"),
            ("大学", 0, "Heiban"),
            ("中国語", 0, "Heiban"),
            ("見物", 0, "Heiban"),
            # Atamadaka (1)
            ("木", 1, "Atamadaka"),
            ("秋", 1, "Atamadaka"),
            ("電気", 1, "Atamadaka"),
            ("文学", 1, "Atamadaka"),
            ("シャーベット", 1, "Atamadaka"),
            ("けんもほろろ", 1, "Atamadaka"),
            # Nakadaka (2, 3, ...)
            ("花", 2, "Nakadaka"),
            ("お菓子", 2, "Nakadaka"),
            ("雪国", 2, "Nakadaka"),
            ("普及率", 2, "Nakadaka"),
            ("お巡りさん", 2, "Nakadaka"),
            ("金婚式", 2, "Nakadaka"),
            ("国語辞典", 2, "Nakadaka"),
            # Odaka (drop after last mora)
            ("男", 3, "Odaka"),
            ("弟", 4, "Odaka"),
            ("桃の花", 5, "Odaka"),
        ]
    
    def test_ojad_chart_examples(self):
        """Test OJAD with chart-based examples"""
        print("\nTesting OJAD with chart-based examples...")
        
        for word, expected_drop, expected_type in self.test_cases:
            print(f"\nWord: {word}")
            result = self.db.lookup_with_cache(word)
            if result:
                print(f"  Reading: {result['reading']}")
                print(f"  Drop pos: {result['drop_pos']} (expected: {expected_drop})")
                print(f"  Mora count: {result['num_mora']}")
                # Handle both cached and fresh results
                pitch_type_label = result.get('pitch_type_label', PITCH_TYPE_LABELS[result['pitch_type']])
                print(f"  Type: {pitch_type_label} (expected: {expected_type})")
            else:
                print("  Failed to get info")

    def test_ojad_html_parsing(self):
        """Test OJAD HTML parsing functionality"""
        # This test is commented out in the original but could be useful
        pass

if __name__ == '__main__':
    unittest.main() 