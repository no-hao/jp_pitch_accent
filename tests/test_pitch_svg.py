import unittest
from pitch_svg import get_pitch_pattern, generate_pitch_svg, generate_pitch_html

class TestPitchSVG(unittest.TestCase):
    def test_heiban_pattern(self):
        # 平板式 (type 0)
        self.assertEqual(get_pitch_pattern(1, 0), ['L'])
        self.assertEqual(get_pitch_pattern(2, 0), ['L', 'H'])
        self.assertEqual(get_pitch_pattern(3, 0), ['L', 'H', 'H'])
        self.assertEqual(get_pitch_pattern(4, 0), ['L', 'H', 'H', 'H'])

    def test_atamadaka_pattern(self):
        # 頭高型 (type 1)
        self.assertEqual(get_pitch_pattern(1, 1), ['H'])
        self.assertEqual(get_pitch_pattern(2, 1), ['H', 'L'])
        self.assertEqual(get_pitch_pattern(3, 1), ['H', 'L', 'L'])
        self.assertEqual(get_pitch_pattern(4, 1), ['H', 'L', 'L', 'L'])

    def test_nakadaka_pattern(self):
        # 中高型 (type 2)
        self.assertEqual(get_pitch_pattern(1, 2), ['L'])  # Too short
        self.assertEqual(get_pitch_pattern(2, 2), ['L', 'L'])  # Too short
        self.assertEqual(get_pitch_pattern(3, 2), ['L', 'H', 'L'])
        self.assertEqual(get_pitch_pattern(4, 2), ['L', 'H', 'L', 'L'])

    def test_odaka_pattern(self):
        # 尾高型 (type 3)
        self.assertEqual(get_pitch_pattern(1, 3), ['H'])
        self.assertEqual(get_pitch_pattern(2, 3), ['L', 'H'])
        self.assertEqual(get_pitch_pattern(3, 3), ['L', 'H', 'H'])
        self.assertEqual(get_pitch_pattern(4, 3), ['L', 'H', 'H', 'H'])

    def test_svg_scaling(self):
        # Test that SVG scales with text length
        pattern = ['L', 'H', 'H']
        svg1 = generate_pitch_svg(pattern)  # No text length
        svg2 = generate_pitch_svg(pattern, text_length=6)  # Longer text
        self.assertIn('width="', svg1)
        self.assertIn('width="', svg2)
        # SVG with text_length should be wider
        width1 = float(svg1[svg1.find('width="')+7:svg1.find('"', svg1.find('width="')+7)])
        width2 = float(svg2[svg2.find('width="')+7:svg2.find('"', svg2.find('width="')+7)])
        self.assertGreater(width2, width1)

    def test_empty_pattern(self):
        self.assertEqual(get_pitch_pattern(0, 0), [])
        self.assertEqual(generate_pitch_svg([]), "")
        
    def test_basic_patterns(self):
        # Test heiban (平板式)
        svg = generate_pitch_svg(['L', 'H'])
        self.assertIn('<svg', svg)
        self.assertIn('</svg>', svg)
        self.assertIn('<circle', svg)
        self.assertIn('fill="white"', svg)  # Low pitch circle
        self.assertIn('fill="black"', svg)  # High pitch circle
        
        # Test atamadaka (頭高型)
        svg = generate_pitch_svg(['H', 'L'])
        self.assertIn('<svg', svg)
        self.assertIn('</svg>', svg)
        self.assertIn('fill="black"', svg)  # High pitch circle
        self.assertIn('fill="white"', svg)  # Low pitch circle
        
    def test_html_wrapper(self):
        html = generate_pitch_html(['H', 'L'])
        self.assertIn('<div', html)
        self.assertIn('</div>', html)
        self.assertIn('<svg', html)
        
    def test_connecting_lines(self):
        svg = generate_pitch_svg(['H', 'L', 'L'])
        self.assertIn('<path', svg)
        self.assertIn('stroke="black"', svg)
        self.assertIn('fill="none"', svg)

if __name__ == '__main__':
    unittest.main() 