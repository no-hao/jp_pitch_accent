#!/usr/bin/env python3
"""
SVG Generation Test for Japanese Pitch Accent Addon
Tests the pitch accent visualization functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pitch_svg import get_pitch_pattern, generate_pitch_svg, generate_pitch_html
from pitch_db import PitchDB

def test_svg_generation():
    """Test SVG generation for pitch accent visualization"""
    print("=== SVG Generation Test ===\n")
    
    db = PitchDB()
    
    # Test cases: (word, expected_pattern_description)
    test_cases = [
        ("大学", "Heiban - flat pattern"),
        ("木", "Atamadaka - high first, then drop"),
        ("お菓子", "Nakadaka - middle high"),
        ("男", "Odaka - high until end"),
    ]
    
    print("1. Testing Pitch Pattern Generation:")
    print("-" * 40)
    
    for word, description in test_cases:
        print(f"\nWord: {word} ({description})")
        
        # Get pitch data
        result = db.lookup_with_cache(word)
        if not result:
            print("  ❌ No pitch data available")
            continue
        
        drop_pos = result['drop_pos']
        num_mora = result['num_mora']
        
        print(f"  Drop pos: {drop_pos}, Mora count: {num_mora}")
        
        # Convert drop_pos to pitch_type
        from pitch_db import drop_pos_to_type
        pitch_type = drop_pos_to_type(drop_pos, num_mora)
        
        # Generate pitch pattern
        pattern = get_pitch_pattern(num_mora, pitch_type)
        print(f"  Pattern: {pattern}")
        
        # Generate SVG
        svg = generate_pitch_svg(pattern)
        if svg:
            print(f"  SVG: Generated ({len(svg)} characters)")
            # Check for key SVG elements
            if 'svg' in svg and 'circle' in svg:
                print("  ✅ SVG structure looks correct")
            else:
                print("  ❌ SVG structure missing key elements")
        else:
            print("  ❌ SVG generation failed")
    
    print("\n" + "=" * 50)
    print("2. Testing HTML Generation:")
    print("-" * 40)
    
    # Test HTML generation with hover functionality
    test_word = "大学"
    result = db.lookup_with_cache(test_word)
    
    if result:
        drop_pos = result['drop_pos']
        num_mora = result['num_mora']
        
        print(f"\nGenerating HTML for: {test_word}")
        # Convert drop_pos to pitch_type
        from pitch_db import drop_pos_to_type
        pitch_type = drop_pos_to_type(drop_pos, num_mora)
        pattern = get_pitch_pattern(num_mora, pitch_type)
        html = generate_pitch_html(pattern)
        
        if html:
            print(f"  HTML: Generated ({len(html)} characters)")
            
            # Check for key HTML elements
            checks = [
                ('div', 'Container div'),
                ('svg', 'SVG element'),
                ('circle', 'Circle elements'),
                ('hover', 'Hover functionality'),
            ]
            
            for element, description in checks:
                if element in html.lower():
                    print(f"    ✅ {description} found")
                else:
                    print(f"    ❌ {description} missing")
        else:
            print("  ❌ HTML generation failed")
    
    print("\n" + "=" * 50)
    print("3. Testing Edge Cases:")
    print("-" * 40)
    
    # Test edge cases
    edge_cases = [
        (0, 1, "Single mora Heiban"),
        (1, 1, "Single mora Atamadaka"),
        (0, 10, "Long Heiban word"),
        (5, 10, "Long Nakadaka word"),
    ]
    
    for drop_pos, num_mora, description in edge_cases:
        print(f"\nEdge case: {description}")
        print(f"  Drop pos: {drop_pos}, Mora count: {num_mora}")
        
        try:
            # Convert drop_pos to pitch_type
            from pitch_db import drop_pos_to_type
            pitch_type = drop_pos_to_type(drop_pos, num_mora)
            pattern = get_pitch_pattern(num_mora, pitch_type)
            print(f"  Pattern: {pattern}")
            
            svg = generate_pitch_svg(pattern)
            if svg:
                print(f"  SVG: Generated successfully")
            else:
                print(f"  SVG: Failed to generate")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("4. Testing Visual Consistency:")
    print("-" * 40)
    
    # Test that similar patterns generate consistent SVGs
    print("\nTesting visual consistency...")
    
    # Compare two Heiban words
    heiban_words = ["大学", "水"]
    heiban_svgs = []
    
    for word in heiban_words:
        result = db.lookup_with_cache(word)
        if result and result['pitch_type'] == 0:  # Heiban
            pattern = get_pitch_pattern(result['num_mora'], result['pitch_type'])
            svg = generate_pitch_svg(pattern)
            if svg:
                heiban_svgs.append(svg)
                print(f"  {word}: SVG generated")
    
    if len(heiban_svgs) >= 2:
        # Check if they have similar structure (both should be flat patterns)
        if 'circle' in heiban_svgs[0] and 'circle' in heiban_svgs[1]:
            print("  ✅ Heiban SVGs have consistent structure")
        else:
            print("  ❌ Heiban SVGs inconsistent")
    
    print("\n" + "=" * 50)
    print("5. Testing Performance:")
    print("-" * 40)
    
    # Test SVG generation performance
    import time
    
    test_words = ["大学", "木", "お菓子", "男"]
    
    print(f"\nTesting SVG generation for {len(test_words)} words...")
    start_time = time.time()
    
    for word in test_words:
        result = db.lookup_with_cache(word)
        if result:
            pattern = get_pitch_pattern(result['num_mora'], result['pitch_type'])
            svg = generate_pitch_svg(pattern)
            if svg:
                print(f"  {word}: SVG generated")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nTotal time: {duration:.3f} seconds")
    print(f"Average per word: {duration/len(test_words):.3f} seconds")
    
    if duration < 1.0:  # Should be very fast
        print("  ✅ SVG generation performance acceptable")
    else:
        print("  ⚠️ SVG generation might be slow")

if __name__ == '__main__':
    test_svg_generation() 