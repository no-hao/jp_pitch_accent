#!/usr/bin/env python3
"""
MVP Integration Tests for Japanese Pitch Accent Anki Addon
Tests the core functionality that users will actually use.
"""

import unittest
import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pitch_db import PitchDB
from sentence_pitch_processor import SentencePitchProcessor

class TestMVPIntegration(unittest.TestCase):
    """Test the complete MVP workflow that users will experience"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = PitchDB()
        self.processor = SentencePitchProcessor()
        
        # Test cases: (input_text, expected_reading, expected_pitch_info)
        self.test_cases = [
            # Single words - basic functionality
            ("大学", "だいがく", {"pitch_type": 0, "pattern": "Heiban"}),
            ("木", "き", {"pitch_type": 1, "pattern": "Atamadaka"}),
            ("お菓子", "おかし", {"pitch_type": 2, "pattern": "Nakadaka"}),
            ("男", "おとこ", {"pitch_type": 3, "pattern": "Odaka"}),
            
            # Verbs - important for language learning
            ("食べる", "たべる", {"pitch_type": 2, "pattern": "Nakadaka"}),
            ("見る", "みる", {"pitch_type": 1, "pattern": "Atamadaka"}),
            ("行く", "いく", {"pitch_type": 0, "pattern": "Heiban"}),
            
            # Common nouns
            ("日本語", "にほんご", {"pitch_type": 0, "pattern": "Heiban"}),
            ("会社", "かいしゃ", {"pitch_type": 0, "pattern": "Heiban"}),
            ("電気", "でんき", {"pitch_type": 1, "pattern": "Atamadaka"}),
        ]
        
        # Test sentence processing (what users will actually do)
        self.test_sentences = [
            "大学に行きます",
            "私は日本語を勉強しています",
            "お菓子を食べる",
        ]
    
    def test_single_word_processing(self):
        """Test single word processing"""
        print("=== MVP Integration Tests ===\n")
        print("1. Testing Single Word Processing:")
        print("-" * 40)
        
        for word, expected_reading, expected_pitch in self.test_cases:
            print(f"\nInput: {word}")
            
            # Test tokenization
            tokens = self.processor._tokenize(word)
            if not tokens:
                print("  ❌ Tokenization failed")
                continue
                
            token = tokens[0]
            print(f"  Tokenized: {token['surface']} → {token['dict_form']}")
            
            # Test pitch lookup
            result = self.db.lookup_with_cache(word)
            if not result:
                print("  ❌ Pitch lookup failed")
                continue
                
            # Verify results
            reading_match = result['reading'] == expected_reading
            pitch_match = result['pitch_type'] == expected_pitch['pitch_type']
            
            print(f"  Reading: {result['reading']} (expected: {expected_reading}) {'✅' if reading_match else '❌'}")
            print(f"  Pitch: {result['pitch_type']} ({expected_pitch['pattern']}) {'✅' if pitch_match else '❌'}")
            print(f"  Drop pos: {result['drop_pos']}, Mora count: {result['num_mora']}")
            
            if reading_match and pitch_match:
                print("  ✅ PASS")
            else:
                print("  ❌ FAIL")
    
    def test_sentence_processing(self):
        """Test sentence processing"""
        print("\n" + "=" * 50)
        print("2. Testing Sentence Processing:")
        print("-" * 40)
        
        for sentence in self.test_sentences:
            print(f"\nSentence: {sentence}")
            
            # Tokenize the sentence
            tokens = self.processor._tokenize(sentence)
            print(f"  Tokens: {len(tokens)} found")
            
            # Process each content word (skip particles, etc.)
            content_words = []
            for token in tokens:
                pos = token['pos']
                # Focus on nouns, verbs, adjectives
                if pos[0] in ['名詞', '動詞', '形容詞']:
                    content_words.append(token)
            
            print(f"  Content words: {len(content_words)}")
            
            # Get pitch data for content words
            for token in content_words:
                word = token['surface']
                result = self.db.lookup_with_cache(word)
                if result:
                    print(f"    {word}: {result['reading']} (pitch: {result['pitch_type']})")
                else:
                    print(f"    {word}: {token['reading']} (no pitch data)")
    
    def test_cache_functionality(self):
        """Test cache functionality"""
        print("\n" + "=" * 50)
        print("3. Testing Cache Functionality:")
        print("-" * 40)
        
        test_word = "大学"
        print(f"\nTesting cache for: {test_word}")
        
        # First lookup (should hit OJAD)
        start_time = time.time()
        result1 = self.db.lookup_with_cache(test_word)
        time1 = time.time() - start_time
        
        # Second lookup (should hit cache)
        start_time = time.time()
        result2 = self.db.lookup_with_cache(test_word)
        time2 = time.time() - start_time
        
        if result1 and result2:
            print(f"  First lookup: {time1:.3f}s")
            print(f"  Second lookup: {time2:.3f}s")
            print(f"  Cache speedup: {time1/time2:.1f}x faster")
            
            if time2 < time1 * 0.1:  # Cache should be at least 10x faster
                print("  ✅ Cache working effectively")
            else:
                print("  ⚠️ Cache might not be working optimally")
        else:
            print("  ❌ Lookup failed")
    
    def test_persistence(self):
        """Test data persistence"""
        print("\n" + "=" * 50)
        print("4. Testing Data Persistence:")
        print("-" * 40)
        
        test_word = "テスト"
        test_data = {
            'reading': 'てすと',
            'pitch_type': 0,
            'drop_pos': 0,
            'num_mora': 3
        }
        
        print(f"\nTesting persistence for: {test_word}")
        
        # Add test entry
        self.db.add_entry(test_word, **test_data)
        
        # Verify it's saved
        result = self.db.lookup(test_word)
        if result and result['reading'] == test_data['reading']:
            print("  ✅ Data persisted correctly")
        else:
            print("  ❌ Data persistence failed")
        
        # Clean up
        if test_word in self.db.db:
            del self.db.db[test_word]

if __name__ == '__main__':
    unittest.main() 