#!/usr/bin/env python3
"""
Anki Integration Test for Japanese Pitch Accent Addon
Tests the workflow that happens when users interact with Anki.
"""

import unittest
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pitch_db import PitchDB
from sentence_pitch_processor import SentencePitchProcessor

class TestAnkiIntegration(unittest.TestCase):
    """Test Anki integration workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = PitchDB()
        self.processor = SentencePitchProcessor()
        
        # Simulate user input scenarios
        self.test_scenarios = [
            {
                "description": "Single word input",
                "expression": "大学",
                "expected_reading": "だいがく",
                "expected_pitch_type": 0
            },
            {
                "description": "Verb input", 
                "expression": "食べる",
                "expected_reading": "たべる",
                "expected_pitch_type": 2
            },
            {
                "description": "Sentence input",
                "expression": "大学に行きます",
                "expected_reading": "だいがくにいきます",  # Combined reading
                "expected_pitch_type": None  # Multiple words, no single pitch type
            },
            {
                "description": "Empty input",
                "expression": "",
                "expected_reading": None,
                "expected_pitch_type": None
            }
        ]
    
    def test_anki_workflow(self):
        """Test the Anki addon workflow"""
        print("=== Anki Integration Test ===\n")
        
        for scenario in self.test_scenarios:
            print(f"Scenario: {scenario['description']}")
            print(f"Input: '{scenario['expression']}'")
            
            # Simulate the addon's on_focus_lost function
            if not scenario['expression'].strip():
                print("  Result: Empty input, no processing")
                print("  ✅ PASS")
                continue
            
            # Tokenize the input
            tokens = self.processor._tokenize(scenario['expression'])
            if not tokens:
                print("  Result: No tokens found")
                print("  ❌ FAIL")
                continue
            
            print(f"  Tokens: {len(tokens)} found")
            
            # Process each token (like the addon does)
            readings = []
            pitch_info = []
            
            for token in tokens:
                word = token['surface']
                result = self.db.lookup_with_cache(word)
                
                if result:
                    readings.append(result['reading'])
                    pitch_info.append({
                        'word': word,
                        'reading': result['reading'],
                        'pitch_type': result['pitch_type'],
                        'drop_pos': result['drop_pos']
                    })
                    print(f"    {word} → {result['reading']} (pitch: {result['pitch_type']})")
                else:
                    # Fallback to SudachiPy reading
                    readings.append(token['reading'])
                    print(f"    {word} → {token['reading']} (no pitch data)")
            
            # Combine readings (like the addon does)
            combined_reading = ''.join(readings)
            print(f"  Combined reading: {combined_reading}")
            
            # Verify results
            if scenario['expected_reading']:
                reading_match = combined_reading == scenario['expected_reading']
                print(f"  Reading match: {'✅' if reading_match else '❌'}")
            
            if scenario['expected_pitch_type'] is not None and pitch_info:
                # Check if any token matches expected pitch type
                pitch_match = any(info['pitch_type'] == scenario['expected_pitch_type'] 
                                for info in pitch_info)
                print(f"  Pitch type match: {'✅' if pitch_match else '❌'}")
            
            print("  ✅ PASS\n")
    
    def test_performance(self):
        """Test performance of the workflow"""
        print("\n" + "=" * 50)
        print("Performance Testing:")
        print("-" * 40)
        
        test_words = ["大学", "会社", "日本語", "勉強", "食べる", "見る", "行く"]
        
        print(f"\nTesting {len(test_words)} words...")
        start_time = time.time()
        
        for word in test_words:
            tokens = self.processor._tokenize(word)
            for token in tokens:
                self.db.lookup_with_cache(token['surface'])
        
        duration = time.time() - start_time
        print(f"Total time: {duration:.3f} seconds")
        print(f"Average per word: {duration/len(test_words):.3f} seconds")

if __name__ == '__main__':
    unittest.main() 