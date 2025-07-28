#!/usr/bin/env python3
"""
Comprehensive test comparing our pitch accent logic with the Japanese pitch accent chart.
Tests all examples from the chart to ensure perfect matching.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pitch_svg import get_pitch_pattern, get_accent_position, generate_pitch_svg, generate_pitch_html

class TestChartComparison(unittest.TestCase):
    """Test our pitch accent logic against the chart examples"""
    
    def setUp(self):
        """Set up test fixtures with all chart examples"""
        
        # All examples from the Japanese pitch accent chart
        # Format: (word, reading, mora_count, drop_pos, expected_pitch_pattern, expected_accent_positions, description)
        self.chart_examples = [
            # 一拍語 (1 mora)
            ("ナ", "な", 1, 0, ['L'], [False], "1-mora Heiban"),
            ("キ", "き", 1, 1, ['H'], [True], "1-mora Atamadaka"),
            
            # 二拍語 (2 morae)
            ("ミズ", "みず", 2, 0, ['L', 'H'], [False, False], "2-mora Heiban"),
            ("アキ", "あき", 2, 1, ['H', 'L'], [True, False], "2-mora Atamadaka"),
            ("ハナ", "はな", 2, 2, ['L', 'H'], [False, True], "2-mora Odaka"),
            
            # 三拍語 (3 morae)
            ("カイシャ", "かいしゃ", 3, 0, ['L', 'H', 'H'], [False, False, False], "3-mora Heiban"),
            ("デンキ", "でんき", 3, 1, ['H', 'L', 'L'], [True, False, False], "3-mora Atamadaka"),
            ("オカシ", "おかし", 3, 2, ['L', 'H', 'L'], [False, True, False], "3-mora Nakadaka"),
            ("オトコ", "おとこ", 3, 3, ['L', 'H', 'H'], [False, False, True], "3-mora Odaka"),
            
            # 四拍語 (4 morae)
            ("ダイガク", "だいがく", 4, 0, ['L', 'H', 'H', 'H'], [False, False, False, False], "4-mora Heiban"),
            ("ブンガク", "ぶんがく", 4, 1, ['H', 'L', 'L', 'L'], [True, False, False, False], "4-mora Atamadaka"),
            ("ユキグニ", "ゆきぐに", 4, 2, ['L', 'H', 'L', 'L'], [False, True, False, False], "4-mora Nakadaka"),
            ("サイジキ", "さいじき", 4, 3, ['L', 'H', 'H', 'L'], [False, False, True, False], "4-mora Nakadaka"),
            ("オトオト", "おとうと", 4, 4, ['L', 'H', 'H', 'H'], [False, False, False, True], "4-mora Odaka"),
            
            # 五拍語 (5 morae)
            ("チュウゴクゴ", "ちゅうごくご", 5, 0, ['L', 'H', 'H', 'H', 'H'], [False, False, False, False, False], "5-mora Heiban"),
            ("シャアベット", "しゃあべっと", 5, 1, ['H', 'L', 'L', 'L', 'L'], [True, False, False, False, False], "5-mora Atamadaka"),
            ("フキュウリツ", "ふきゅうりつ", 5, 2, ['L', 'H', 'L', 'L', 'L'], [False, True, False, False, False], "5-mora Nakadaka"),
            ("ヤマノボリ", "やまのぼり", 5, 3, ['L', 'H', 'H', 'L', 'L'], [False, False, True, False, False], "5-mora Nakadaka"),
            ("コガタバス", "こがたばす", 5, 4, ['L', 'H', 'H', 'H', 'L'], [False, False, False, True, False], "5-mora Nakadaka"),
            ("モモノハナ", "もものはな", 5, 5, ['L', 'H', 'H', 'H', 'H'], [False, False, False, False, True], "5-mora Odaka"),
            
            # 六拍語 (6 morae)
            ("ケンブツニン", "けんぶつにん", 6, 0, ['L', 'H', 'H', 'H', 'H', 'H'], [False, False, False, False, False, False], "6-mora Heiban"),
            ("ケンモホロロ", "けんもほろろ", 6, 1, ['H', 'L', 'L', 'L', 'L', 'L'], [True, False, False, False, False, False], "6-mora Atamadaka"),
            ("オマワリサン", "おまわりさん", 6, 2, ['L', 'H', 'L', 'L', 'L', 'L'], [False, True, False, False, False, False], "6-mora Nakadaka"),
            ("キンコンシキ", "きんこんしき", 6, 3, ['L', 'H', 'H', 'L', 'L', 'L'], [False, False, True, False, False, False], "6-mora Nakadaka"),
            ("コクゴジテン", "こくごじてん", 6, 4, ['L', 'H', 'H', 'H', 'L', 'L'], [False, False, False, True, False, False], "6-mora Nakadaka"),
            ("タンサンガス", "たんさんがす", 6, 5, ['L', 'H', 'H', 'H', 'H', 'L'], [False, False, False, False, True, False], "6-mora Nakadaka"),
            ("ジュウイチガツ", "じゅういちがつ", 6, 6, ['L', 'H', 'H', 'H', 'H', 'H'], [False, False, False, False, False, True], "6-mora Odaka"),
        ]
    
    def test_all_chart_examples(self):
        """Test all examples from the chart"""
        print("🎯 Testing All Chart Examples")
        print("=" * 60)
        print("Comparing our logic with the Japanese pitch accent chart...\n")
        
        all_passed = True
        passed_count = 0
        total_count = len(self.chart_examples)
        
        for word, reading, mora_count, drop_pos, expected_pattern, expected_accent_positions, description in self.chart_examples:
            print(f"\n📝 {word} ({reading}) - {description}")
            print(f"   Mora count: {mora_count}, Drop position: {drop_pos}")
            
            # Generate our results
            actual_pattern = get_pitch_pattern(mora_count, drop_pos)
            actual_accent_positions = get_accent_position(mora_count, drop_pos)
            
            # Test pitch pattern
            pattern_passed = actual_pattern == expected_pattern
            print(f"   Pitch pattern: {actual_pattern}")
            print(f"   Expected:      {expected_pattern}")
            print(f"   Pattern:       {'✅ PASS' if pattern_passed else '❌ FAIL'}")
            
            # Test accent positions
            accent_passed = actual_accent_positions == expected_accent_positions
            print(f"   Accent pos:    {actual_accent_positions}")
            print(f"   Expected:      {expected_accent_positions}")
            print(f"   Accent:        {'✅ PASS' if accent_passed else '❌ FAIL'}")
            
            # Generate visual representation
            visual = ""
            height_visual = ""
            for pitch, is_accent in zip(actual_pattern, actual_accent_positions):
                if is_accent:
                    visual += "○"  # White accent dot
                else:
                    visual += "●"  # Black normal dot
                height_visual += "↑" if pitch == 'H' else "↓"
            
            print(f"   Visual:        {visual}")
            print(f"   Height:        {height_visual}")
            
            # Test SVG generation
            try:
                svg = generate_pitch_svg(actual_pattern, actual_accent_positions)
                svg_passed = len(svg) > 0 and '<svg' in svg
                print(f"   SVG:           {'✅ Generated' if svg_passed else '❌ Failed'}")
            except Exception as e:
                svg_passed = False
                print(f"   SVG:           ❌ Error: {e}")
            
            # Overall test result
            test_passed = pattern_passed and accent_passed and svg_passed
            if test_passed:
                passed_count += 1
                print(f"   Overall:       ✅ PASS")
            else:
                all_passed = False
                print(f"   Overall:       ❌ FAIL")
            
            print("-" * 40)
        
        # Summary
        print(f"\n📊 Test Summary")
        print("=" * 40)
        print(f"Total examples: {total_count}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {total_count - passed_count}")
        print(f"Success rate: {(passed_count/total_count)*100:.1f}%")
        
        if all_passed:
            print(f"\n🎉 ALL TESTS PASSED! Our logic perfectly matches the chart!")
        else:
            print(f"\n⚠️  Some tests failed. Check the output above for details.")
        
        self.assertTrue(all_passed, f"Only {passed_count}/{total_count} chart examples passed")
    
    def test_pitch_type_categories(self):
        """Test each pitch accent type category"""
        print("\n\n🎵 Testing Pitch Accent Type Categories")
        print("=" * 50)
        
        # Group examples by pitch type
        categories = {
            "Heiban (平板式)": [],
            "Atamadaka (頭高型)": [],
            "Nakadaka (中高型)": [],
            "Odaka (尾高型)": []
        }
        
        for example in self.chart_examples:
            word, reading, mora_count, drop_pos, expected_pattern, expected_accent_positions, description = example
            
            if drop_pos == 0:
                categories["Heiban (平板式)"].append(example)
            elif drop_pos == 1:
                categories["Atamadaka (頭高型)"].append(example)
            elif drop_pos == mora_count:
                categories["Odaka (尾高型)"].append(example)
            else:
                categories["Nakadaka (中高型)"].append(example)
        
        for category_name, examples in categories.items():
            print(f"\n{category_name}:")
            print(f"  Examples: {len(examples)}")
            
            for word, reading, mora_count, drop_pos, expected_pattern, expected_accent_positions, description in examples:
                actual_pattern = get_pitch_pattern(mora_count, drop_pos)
                actual_accent_positions = get_accent_position(mora_count, drop_pos)
                
                # Create visual representation
                visual = ""
                height_visual = ""
                for pitch, is_accent in zip(actual_pattern, actual_accent_positions):
                    if is_accent:
                        visual += "○"
                    else:
                        visual += "●"
                    height_visual += "↑" if pitch == 'H' else "↓"
                
                print(f"    {word} ({reading}): {visual} | {height_visual}")
    
    def test_mora_count_groups(self):
        """Test examples grouped by mora count"""
        print("\n\n📏 Testing by Mora Count Groups")
        print("=" * 40)
        
        # Group by mora count
        mora_groups = {}
        for example in self.chart_examples:
            word, reading, mora_count, drop_pos, expected_pattern, expected_accent_positions, description = example
            if mora_count not in mora_groups:
                mora_groups[mora_count] = []
            mora_groups[mora_count].append(example)
        
        for mora_count in sorted(mora_groups.keys()):
            examples = mora_groups[mora_count]
            print(f"\n{mora_count} Mora Words ({len(examples)} examples):")
            
            for word, reading, mora_count, drop_pos, expected_pattern, expected_accent_positions, description in examples:
                actual_pattern = get_pitch_pattern(mora_count, drop_pos)
                actual_accent_positions = get_accent_position(mora_count, drop_pos)
                
                # Create visual representation
                visual = ""
                height_visual = ""
                for pitch, is_accent in zip(actual_pattern, actual_accent_positions):
                    if is_accent:
                        visual += "○"
                    else:
                        visual += "●"
                    height_visual += "↑" if pitch == 'H' else "↓"
                
                pitch_type = "Heiban" if drop_pos == 0 else "Atamadaka" if drop_pos == 1 else "Odaka" if drop_pos == mora_count else "Nakadaka"
                print(f"  {word} ({reading}): {pitch_type} - {visual} | {height_visual}")

if __name__ == '__main__':
    unittest.main(verbosity=2) 