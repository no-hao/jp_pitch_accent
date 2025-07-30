import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sentence_pitch_processor import SentencePitchProcessor

class TestTokenizer(unittest.TestCase):
    """Test Japanese text tokenization with SudachiPy"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = SentencePitchProcessor()
    
    def test_tokenization(self):
        """Test Japanese text tokenization"""
        print("\nTesting tokenization...")
        
        # Test sentences
        test_texts = [
            '大学に行きます。',
            '私は日本語を勉強しています。',
            '食べる',
            '見る'
        ]
        
        for text in test_texts:
            print(f"\nTokenizing: {text}")
            tokens = self.processor._tokenize(text)
            
            for token in tokens:
                print(f"\nToken:")
                print(f"  Surface:   {token['surface']}")
                print(f"  Dict form: {token['dict_form']}")
                print(f"  Reading:   {token['reading']}")
                print(f"  POS:       {token['pos']}")

if __name__ == '__main__':
    unittest.main() 