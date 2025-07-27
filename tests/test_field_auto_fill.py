#!/usr/bin/env python3
"""
Test Field Auto-Fill Functionality
Tests the auto-fill functionality when typing in the Expression field.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pitch_db import PitchDB
from pitch_tokenizer import JapaneseTokenizer

class TestFieldAutoFill(unittest.TestCase):
    """Test field auto-fill functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = PitchDB()
        self.tokenizer = JapaneseTokenizer()
        
        # Test cases: (input_text, expected_reading, expected_meaning)
        self.test_cases = [
            # Single words
            ("大学", "だいがく", "大学(名詞)"),
            ("食べる", "たべる", "食べる(動詞)"),
            ("美しい", "うつくしい", "美しい(形容詞)"),
            
            # Sentences
            ("大学に行きます", "だいがくにいきます", "大学(名詞) 行き(動詞)"),
            ("私は日本語を勉強しています", "わたしはにほんごをべんきょうしています", "私(名詞) 日本語(名詞) 勉強(名詞)"),
        ]
    
    def test_single_word_processing(self):
        """Test single word auto-fill"""
        print("=== Testing Single Word Auto-Fill ===")
        
        for text, expected_reading, expected_meaning in self.test_cases[:3]:
            print(f"\nInput: {text}")
            
            # Tokenize
            tokens = self.tokenizer.tokenize(text)
            print(f"  Tokens: {tokens}")
            
            # Process tokens (simulate the addon logic)
            readings = []
            meanings = []
            
            for token in tokens:
                surface = token["surface"]
                dict_form = token.get("dict", surface)
                reading = token.get("reading", surface)
                pos = token.get("pos", [])
                
                print(f"    Token: {surface} -> {dict_form} (reading: {reading}, pos: {pos})")
                
                # Skip punctuation
                if all(not self.tokenizer.is_kanji(c) and not self.tokenizer.is_kana(c) for c in surface):
                    readings.append(surface)
                    continue
                
                # Get pitch info
                pitch_info = self.db.lookup_with_cache(dict_form)
                if pitch_info:
                    reading = pitch_info["reading"]
                    readings.append(reading)
                else:
                    readings.append(reading)
                
                # Extract part of speech
                if pos and len(pos) > 0:
                    pos_str = pos[0]
                    if pos_str in ['名詞', '動詞', '形容詞', '副詞']:
                        meanings.append(f"{surface}({pos_str})")
            
            # Combine results
            combined_reading = ''.join(readings)
            combined_meaning = ' '.join(meanings)
            
            print(f"  Reading: {combined_reading}")
            print(f"  Meaning: {combined_meaning}")
            
            # Verify results
            reading_match = combined_reading == expected_reading
            meaning_match = combined_meaning == expected_meaning
            
            print(f"  Reading match: {'✅' if reading_match else '❌'}")
            print(f"  Meaning match: {'✅' if meaning_match else '❌'}")
            
            if reading_match and meaning_match:
                print("  ✅ PASS")
            else:
                print("  ❌ FAIL")
    
    def test_sentence_processing(self):
        """Test sentence auto-fill"""
        print("\n=== Testing Sentence Auto-Fill ===")
        
        for text, expected_reading, expected_meaning in self.test_cases[3:]:
            print(f"\nInput: {text}")
            
            # Tokenize
            tokens = self.tokenizer.tokenize(text)
            print(f"  Tokens: {len(tokens)} found")
            
            # Process tokens (simulate the addon logic)
            readings = []
            meanings = []
            
            for token in tokens:
                surface = token["surface"]
                dict_form = token.get("dict", surface)
                reading = token.get("reading", surface)
                pos = token.get("pos", [])
                
                # Skip punctuation
                if all(not self.tokenizer.is_kanji(c) and not self.tokenizer.is_kana(c) for c in surface):
                    readings.append(surface)
                    continue
                
                # Get pitch info
                pitch_info = self.db.lookup_with_cache(dict_form)
                if pitch_info:
                    reading = pitch_info["reading"]
                    readings.append(reading)
                else:
                    readings.append(reading)
                
                # Extract part of speech
                if pos and len(pos) > 0:
                    pos_str = pos[0]
                    if pos_str in ['名詞', '動詞', '形容詞', '副詞']:
                        meanings.append(f"{surface}({pos_str})")
            
            # Combine results
            combined_reading = ''.join(readings)
            combined_meaning = ' '.join(meanings)
            
            print(f"  Reading: {combined_reading}")
            print(f"  Meaning: {combined_meaning}")
            
            # Verify results
            reading_match = combined_reading == expected_reading
            meaning_match = combined_meaning == expected_meaning
            
            print(f"  Reading match: {'✅' if reading_match else '❌'}")
            print(f"  Meaning match: {'✅' if meaning_match else '❌'}")
            
            if reading_match and meaning_match:
                print("  ✅ PASS")
            else:
                print("  ❌ FAIL")

if __name__ == '__main__':
    unittest.main() 