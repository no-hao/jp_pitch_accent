import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pitch_db import PitchDB, PITCH_TYPE_LABELS

class TestPitchDB(unittest.TestCase):
    """Test PitchDB functionality with SudachiPy"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = PitchDB()
    
    def test_pitch_db_lookup(self):
        """Test PitchDB lookup functionality"""
        print("\nTesting PitchDB...")
        
        # Test words
        test_words = [
            '大学',
            '食べる',
            '行きます',
            '見る',
            '日本語',
            '勉強する'
        ]
        
        for word in test_words:
            print(f"\nAnalyzing word: {word}")
            
            # Try cache first
            print("Checking cache...")
            result = self.db.lookup(word)
            if result:
                print(f"Found in cache: {result}")
                continue
                
            print("Not in cache, analyzing with SudachiPy...")
            result = self.db.lookup_with_cache(word)
            if result:
                print(f"Analysis successful!")
                print(f"Reading: {result['reading']}")
                print(f"Drop position: {result['drop_pos']}")
                print(f"Number of morae: {result['num_mora']}")
                pitch_type_label = result.get('pitch_type_label', PITCH_TYPE_LABELS[result['pitch_type']])
                print(f"Pitch type: {result['pitch_type']} ({pitch_type_label})")
            else:
                print("Analysis failed!")

if __name__ == '__main__':
    unittest.main() 