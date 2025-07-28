import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pitch_svg import get_pitch_pattern, get_accent_position, generate_pitch_svg, generate_pitch_html

class TestPitchSVG(unittest.TestCase):
    def test_heiban_pattern(self):
        # 平板式 (drop_pos = 0) - starts low, goes high, stays high
        self.assertEqual(get_pitch_pattern(1, 0), ['L'])
        self.assertEqual(get_pitch_pattern(2, 0), ['L', 'H'])
        self.assertEqual(get_pitch_pattern(3, 0), ['L', 'H', 'H'])
        self.assertEqual(get_pitch_pattern(4, 0), ['L', 'H', 'H', 'H'])

    def test_atamadaka_pattern(self):
        # 頭高型 (drop_pos = 1) - starts high, drops, stays low
        self.assertEqual(get_pitch_pattern(1, 1), ['H'])
        self.assertEqual(get_pitch_pattern(2, 1), ['H', 'L'])
        self.assertEqual(get_pitch_pattern(3, 1), ['H', 'L', 'L'])
        self.assertEqual(get_pitch_pattern(4, 1), ['H', 'L', 'L', 'L'])

    def test_nakadaka_pattern(self):
        # 中高型 (drop_pos = 2, 3, etc.) - starts low, rises, drops after accent
        self.assertEqual(get_pitch_pattern(2, 2), ['L', 'H'])
        self.assertEqual(get_pitch_pattern(3, 2), ['L', 'H', 'L'])
        self.assertEqual(get_pitch_pattern(4, 2), ['L', 'H', 'L', 'L'])
        self.assertEqual(get_pitch_pattern(4, 3), ['L', 'H', 'H', 'L'])

    def test_odaka_pattern(self):
        # 尾高型 (drop_pos = mora_count) - starts low, rises, stays high
        self.assertEqual(get_pitch_pattern(1, 1), ['H'])
        self.assertEqual(get_pitch_pattern(2, 2), ['L', 'H'])
        self.assertEqual(get_pitch_pattern(3, 3), ['L', 'H', 'H'])
        self.assertEqual(get_pitch_pattern(4, 4), ['L', 'H', 'H', 'H'])

    def test_accent_positions(self):
        # Test accent position logic
        # Heiban - no accent mora
        self.assertEqual(get_accent_position(2, 0), [False, False])
        # Atamadaka - first mora is accent
        self.assertEqual(get_accent_position(2, 1), [True, False])
        # Nakadaka - middle mora is accent
        self.assertEqual(get_accent_position(3, 2), [False, True, False])
        # Odaka - last mora is accent
        self.assertEqual(get_accent_position(3, 3), [False, False, True])

    def test_svg_scaling(self):
        # Test that SVG scales with text length
        pitch_pattern = ['L', 'H', 'H']
        accent_positions = [False, False, False]
        svg1 = generate_pitch_svg(pitch_pattern, accent_positions)  # No text length
        svg2 = generate_pitch_svg(pitch_pattern, accent_positions, text_length=6)  # Longer text
        self.assertIn('width="', svg1)
        self.assertIn('width="', svg2)
        # SVG with text_length should be wider
        width1 = float(svg1[svg1.find('width="')+7:svg1.find('"', svg1.find('width="')+7)])
        width2 = float(svg2[svg2.find('width="')+7:svg2.find('"', svg2.find('width="')+7)])
        self.assertGreater(width2, width1)

    def test_empty_pattern(self):
        self.assertEqual(get_pitch_pattern(0, 0), [])
        self.assertEqual(get_accent_position(0, 0), [])
        self.assertEqual(generate_pitch_svg([], []), "")
        
    def test_basic_patterns(self):
        # Test heiban (平板式) - no accent mora, all black dots
        pitch_pattern = ['L', 'H']
        accent_positions = [False, False]
        svg = generate_pitch_svg(pitch_pattern, accent_positions)
        self.assertIn('<svg', svg)
        self.assertIn('</svg>', svg)
        self.assertIn('<circle', svg)
        self.assertIn('fill="black"', svg)  # All dots should be black
        self.assertNotIn('fill="white"', svg)  # No white dots
        
        # Test atamadaka (頭高型) - first mora is accent (white)
        pitch_pattern = ['H', 'L']
        accent_positions = [True, False]
        svg = generate_pitch_svg(pitch_pattern, accent_positions)
        self.assertIn('<svg', svg)
        self.assertIn('</svg>', svg)
        self.assertIn('fill="white"', svg)  # Accent mora should be white
        self.assertIn('fill="black"', svg)  # Other morae should be black
        
    def test_html_wrapper(self):
        pitch_pattern = ['H', 'L']
        accent_positions = [True, False]
        html = generate_pitch_html(pitch_pattern, accent_positions)
        self.assertIn('<div', html)
        self.assertIn('</div>', html)
        self.assertIn('<svg', html)
        
    def test_connecting_lines(self):
        pitch_pattern = ['H', 'L', 'L']
        accent_positions = [True, False, False]
        svg = generate_pitch_svg(pitch_pattern, accent_positions)
        self.assertIn('<path', svg)
        self.assertIn('stroke="black"', svg)
        self.assertIn('fill="none"', svg)

if __name__ == '__main__':
    unittest.main() 