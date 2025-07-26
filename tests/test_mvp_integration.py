#!/usr/bin/env python3
"""
MVP Integration Tests for Japanese Pitch Accent Anki Addon
Tests the core functionality that users will actually use.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pitch_db import PitchDB
from pitch_tokenizer import JapaneseTokenizer
import json
import os

def test_mvp_integration():
    """Test the complete MVP workflow that users will experience"""
    print("=== MVP Integration Tests ===\n")
    
    # Initialize components
    db = PitchDB()
    tokenizer = JapaneseTokenizer()
    
    # Test cases: (input_text, expected_reading, expected_pitch_info)
    test_cases = [
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
    
    print("1. Testing Single Word Processing:")
    print("-" * 40)
    
    for word, expected_reading, expected_pitch in test_cases:
        print(f"\nInput: {word}")
        
        # Test tokenization
        tokens = tokenizer.tokenize(word)
        if not tokens:
            print("  ❌ Tokenization failed")
            continue
            
        token = tokens[0]
        print(f"  Tokenized: {token['surface']} → {token['dict_form']}")
        
        # Test pitch lookup
        result = db.lookup_with_cache(word)
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
    
    print("\n" + "=" * 50)
    print("2. Testing Sentence Processing:")
    print("-" * 40)
    
    # Test sentence processing (what users will actually do)
    test_sentences = [
        "大学に行きます",
        "私は日本語を勉強しています",
        "お菓子を食べる",
    ]
    
    for sentence in test_sentences:
        print(f"\nSentence: {sentence}")
        
        # Tokenize the sentence
        tokens = tokenizer.tokenize(sentence)
        print(f"  Tokens: {len(tokens)} found")
        
        # Process each content word (skip particles, etc.)
        content_words = []
        for token in tokens:
            pos = token['pos']
            # Focus on nouns, verbs, adjectives
            if pos[0] in ['名詞', '動詞', '形容詞']:
                content_words.append(token)
        
        print(f"  Content words: {len(content_words)}")
        
        # Look up pitch for each content word
        for token in content_words:
            word = token['surface']
            result = db.lookup_with_cache(word)
            if result:
                print(f"    {word}: {result['reading']} ({result['pitch_type']})")
            else:
                print(f"    {word}: ❌ No pitch data")
    
    print("\n" + "=" * 50)
    print("3. Testing Error Handling:")
    print("-" * 40)
    
    # Test edge cases and errors
    edge_cases = [
        "",  # Empty string
        "abc",  # Non-Japanese
        "123",  # Numbers
        "！",  # Punctuation
    ]
    
    for case in edge_cases:
        print(f"\nEdge case: '{case}'")
        
        # Test tokenization
        tokens = tokenizer.tokenize(case)
        if tokens:
            print(f"  Tokens: {len(tokens)} (unexpected)")
        else:
            print(f"  Tokens: None (expected)")
        
        # Test pitch lookup
        result = db.lookup_with_cache(case)
        if result:
            print(f"  Pitch: Found (unexpected)")
        else:
            print(f"  Pitch: None (expected)")
    
    print("\n" + "=" * 50)
    print("4. Testing Cache Functionality:")
    print("-" * 40)
    
    # Test that cache works correctly
    test_word = "大学"
    print(f"\nTesting cache for: {test_word}")
    
    # First lookup (should hit OJAD or cache)
    result1 = db.lookup_with_cache(test_word)
    print(f"  First lookup: {result1['reading'] if result1 else 'None'}")
    
    # Second lookup (should hit cache)
    result2 = db.lookup_with_cache(test_word)
    print(f"  Second lookup: {result2['reading'] if result2 else 'None'}")
    
    # Verify cache consistency
    if result1 and result2 and result1 == result2:
        print("  ✅ Cache working correctly")
    else:
        print("  ❌ Cache inconsistency")
    
    print("\n" + "=" * 50)
    print("5. Testing Database Persistence:")
    print("-" * 40)
    
    # Test that data persists between runs
    test_word = "テスト"
    test_data = {
        "reading": "てすと",
        "drop_pos": 1,
        "num_mora": 3,
        "pitch_type": 1,
        "meaning": "test"
    }
    
    print(f"\nTesting persistence for: {test_word}")
    
    # Add test entry
    db.add_entry(test_word, **test_data)
    print(f"  Added to database")
    
    # Verify it's in cache
    result = db.lookup(test_word)
    if result and result['reading'] == test_data['reading']:
        print("  ✅ Data persisted correctly")
    else:
        print("  ❌ Data persistence failed")
    
    # Clean up test data
    if test_word in db.db:
        del db.db[test_word]
        db.save()
        print("  Cleaned up test data")

if __name__ == '__main__':
    test_mvp_integration() 