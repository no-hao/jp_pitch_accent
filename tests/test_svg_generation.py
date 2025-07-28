#!/usr/bin/env python3
"""
SVG Generation Test for Japanese Pitch Accent Addon
Tests the pitch accent visualization functionality.
"""

import unittest
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pitch_svg import get_pitch_pattern, get_accent_position, generate_pitch_svg, generate_pitch_html
from pitch_db import PitchDB, drop_pos_to_type

class TestSVGGeneration(unittest.TestCase):
    """Test SVG generation for pitch accent visualization"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = PitchDB()
        
        # Test cases: (word, expected_pattern_description)
        self.test_cases = [
            ("大学", "Heiban - starts low, goes high, stays high"),
            ("木", "Atamadaka - starts high, drops after first mora"),
            ("お菓子", "Nakadaka - starts low, rises, drops after second mora"),
            ("男", "Odaka - starts low, rises, stays high until end"),
        ]
    
    def test_pitch_pattern_generation(self):
        """Test pitch pattern generation"""
        print("=== SVG Generation Test ===\n")
        print("1. Testing Pitch Pattern Generation:")
        print("-" * 40)
        
        for word, description in self.test_cases:
            print(f"\nWord: {word} ({description})")
            
            # Get pitch data
            result = self.db.lookup_with_cache(word)
            if not result:
                print("  ❌ No pitch data available")
                continue
            
            drop_pos = result['drop_pos']
            num_mora = result['num_mora']
            
            print(f"  Drop pos: {drop_pos}, Mora count: {num_mora}")
            
            # Generate pitch pattern and accent positions
            pitch_pattern = get_pitch_pattern(num_mora, drop_pos)
            accent_positions = get_accent_position(num_mora, drop_pos)
            print(f"  Pitch pattern: {pitch_pattern}")
            print(f"  Accent positions: {accent_positions}")
            
            # Generate SVG
            svg = generate_pitch_svg(pitch_pattern, accent_positions)
            if svg:
                print(f"  SVG: Generated ({len(svg)} characters)")
                # Check for key SVG elements
                if 'svg' in svg and 'circle' in svg:
                    print("  ✅ SVG structure looks correct")
                    # Check for white/black dots based on accent positions
                    if any(accent_positions):
                        if 'fill="white"' in svg:
                            print("  ✅ White accent dot found")
                        else:
                            print("  ❌ White accent dot missing")
                    if 'fill="black"' in svg:
                        print("  ✅ Black dots found")
                    else:
                        print("  ❌ Black dots missing")
                else:
                    print("  ❌ SVG structure missing key elements")
            else:
                print("  ❌ SVG generation failed")
    
    def test_html_generation(self):
        """Test HTML generation with hover functionality"""
        print("\n" + "=" * 50)
        print("2. Testing HTML Generation:")
        print("-" * 40)
        
        # Test HTML generation with hover functionality
        test_word = "大学"
        result = self.db.lookup_with_cache(test_word)
        
        if result:
            drop_pos = result['drop_pos']
            num_mora = result['num_mora']
            
            print(f"\nGenerating HTML for: {test_word}")
            # Generate pitch pattern and accent positions
            pitch_pattern = get_pitch_pattern(num_mora, drop_pos)
            accent_positions = get_accent_position(num_mora, drop_pos)
            html = generate_pitch_html(pitch_pattern, accent_positions)
            
            if html:
                print(f"  HTML: Generated ({len(html)} characters)")
                
                # Check for key HTML elements
                checks = [
                    ('div', 'Container div'),
                    ('svg', 'SVG element'),
                    ('circle', 'Circle elements'),
                ]
                
                for element, description in checks:
                    if element in html.lower():
                        print(f"    ✅ {description} found")
                    else:
                        print(f"    ❌ {description} missing")
            else:
                print("  ❌ HTML generation failed")
    
    def test_performance(self):
        """Test performance of SVG generation"""
        print("\n" + "=" * 50)
        print("3. Performance Testing:")
        print("-" * 40)
        
        test_words = ["大学", "木", "お菓子", "男"]
        
        print(f"\nTesting SVG generation for {len(test_words)} words...")
        start_time = time.time()
        
        for word in test_words:
            result = self.db.lookup_with_cache(word)
            if result:
                drop_pos = result['drop_pos']
                num_mora = result['num_mora']
                pitch_pattern = get_pitch_pattern(num_mora, drop_pos)
                accent_positions = get_accent_position(num_mora, drop_pos)
                svg = generate_pitch_svg(pitch_pattern, accent_positions)
                html = generate_pitch_html(pitch_pattern, accent_positions)
        
        duration = time.time() - start_time
        print(f"Total time: {duration:.3f} seconds")
        print(f"Average per word: {duration/len(test_words):.3f} seconds")

if __name__ == '__main__':
    unittest.main() 