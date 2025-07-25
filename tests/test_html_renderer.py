import unittest
from html_renderer import render_ruby
from pipeline import annotate_pitch

class TestHtmlRenderer(unittest.TestCase):
    def test_render_ruby(self):
        tokens = [
            {"surface": "食べる", "reading": "たべる", "pitch": 1},
            {"surface": "。", "reading": "", "pitch": None},
        ]
        html = render_ruby(tokens)
        expected = '<ruby>食べる<rt>たべる [1]</rt></ruby>。'
        self.assertEqual(html, expected)

    def test_annotate_pitch_end_to_end(self):
        sentence = "食べる。"
        html = annotate_pitch(sentence)
        expected = '<ruby>食べる<rt>たべる [1]</rt></ruby>。'
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()
