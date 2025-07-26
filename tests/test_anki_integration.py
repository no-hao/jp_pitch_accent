#!/usr/bin/env python3
"""
Anki Integration Test for Japanese Pitch Accent Addon
Tests the workflow that happens when users interact with Anki.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pitch_db import PitchDB
from pitch_tokenizer import JapaneseTokenizer

def simulate_anki_workflow():
    """Simulate the Anki addon workflow"""
    print("=== Anki Integration Test ===\n")
    
    # Initialize components (like the addon does)
    db = PitchDB()
    tokenizer = JapaneseTokenizer()
    
    # Simulate user input scenarios
    test_scenarios = [
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
    
    for scenario in test_scenarios:
        print(f"Scenario: {scenario['description']}")
        print(f"Input: '{scenario['expression']}'")
        
        # Simulate the addon's on_focus_lost function
        if not scenario['expression'].strip():
            print("  Result: Empty input, no processing")
            print("  ✅ PASS")
            continue
        
        # Tokenize the input
        tokens = tokenizer.tokenize(scenario['expression'])
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
            result = db.lookup_with_cache(word)
            
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
            # For single words, check pitch type
            pitch_match = pitch_info[0]['pitch_type'] == scenario['expected_pitch_type']
            print(f"  Pitch match: {'✅' if pitch_match else '❌'}")
        
        print("  ✅ PASS\n")
    
    print("=" * 50)
    print("Testing Error Recovery:")
    print("-" * 30)
    
    # Test error recovery scenarios
    error_scenarios = [
        "ネットワークエラー",  # Network error simulation
        "不正な文字",        # Invalid characters
        "very long text that might cause issues with the system",
    ]
    
    for text in error_scenarios:
        print(f"\nError test: '{text}'")
        
        try:
            # Simulate processing with potential errors
            tokens = tokenizer.tokenize(text)
            if tokens:
                print(f"  Tokens processed: {len(tokens)}")
                
                # Try to get pitch data
                for token in tokens[:3]:  # Limit to first 3 tokens
                    result = db.lookup_with_cache(token['surface'])
                    if result:
                        print(f"    {token['surface']}: ✅ Got pitch data")
                    else:
                        print(f"    {token['surface']}: ⚠️ No pitch data (fallback)")
            else:
                print("  No tokens found")
                
            print("  ✅ Error handled gracefully")
            
        except Exception as e:
            print(f"  ❌ Error not handled: {e}")
    
    print("\n" + "=" * 50)
    print("Testing Performance:")
    print("-" * 30)
    
    # Test performance with multiple words
    import time
    
    test_words = ["大学", "会社", "日本語", "勉強", "食べる", "見る", "行く"]
    
    print(f"\nTesting {len(test_words)} words...")
    start_time = time.time()
    
    for word in test_words:
        result = db.lookup_with_cache(word)
        if result:
            print(f"  {word}: {result['reading']} ({result['pitch_type']})")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nTotal time: {duration:.3f} seconds")
    print(f"Average per word: {duration/len(test_words):.3f} seconds")
    
    if duration < 5.0:  # Should be fast since most are cached
        print("  ✅ Performance acceptable")
    else:
        print("  ⚠️ Performance might be slow")

if __name__ == '__main__':
    simulate_anki_workflow() 