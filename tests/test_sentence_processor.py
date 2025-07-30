#!/usr/bin/env python3
"""
Tests for sentence-level pitch accent processor.
Validates the processor against known Japanese pitch accent rules.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_pitch_processor import SentencePitchProcessor


class TestSentencePitchProcessor(unittest.TestCase):
    """Test cases for the SentencePitchProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = SentencePitchProcessor()

    def test_basic_sentence_processing(self):
        """Test basic sentence processing."""
        sentence = "大学に行きます"
        result = self.processor.process_sentence(sentence)
        
        self.assertIsNotNone(result)
        self.assertIn('reading', result)
        self.assertIn('pattern', result)
        self.assertIn('accent_positions', result)
        
        # Check that we get the correct reading
        self.assertEqual(result['reading'], 'だいがくにいきます')
        
        # Check that we have a pattern
        self.assertIsInstance(result['pattern'], list)
        self.assertGreater(len(result['pattern']), 0)

    def test_conjugated_verb_processing(self):
        """Test processing of conjugated verbs."""
        sentence = "お菓子を食べる"
        result = self.processor.process_sentence(sentence)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['reading'], 'おかしをたべる')
        
        # Should have accents on both words
        accent_count = sum(result['accent_positions'])
        self.assertGreaterEqual(accent_count, 1)

    def test_multiple_phrase_sentence(self):
        """Test sentence with multiple phrases."""
        sentence = "私は日本語を勉強しています"
        result = self.processor.process_sentence(sentence)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['reading'], 'わたしはにほんごをべんきょうしています')

    def test_complex_conjugation(self):
        """Test complex verb conjugations."""
        sentence = "新しい本を買いました"
        result = self.processor.process_sentence(sentence)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['reading'], 'あたらしいほんをかいました')

    def test_empty_sentence(self):
        """Test empty sentence handling."""
        result = self.processor.process_sentence("")
        self.assertIsNotNone(result)
        self.assertEqual(result['reading'], '')

    def test_single_word(self):
        """Test single word processing."""
        result = self.processor.process_sentence("大学")
        self.assertIsNotNone(result)
        self.assertEqual(result['reading'], 'だいがく')

    def test_svg_generation(self):
        """Test SVG generation."""
        sentence = "大学に行きます"
        svg = self.processor.generate_sentence_svg(sentence)
        
        self.assertIsInstance(svg, str)
        self.assertIn('<svg', svg)
        self.assertIn('</svg>', svg)

    def test_html_generation(self):
        """Test HTML generation."""
        sentence = "大学に行きます"
        html = self.processor.generate_sentence_html(sentence)
        
        self.assertIsInstance(html, str)
        self.assertIn('<div', html)
        self.assertIn('</div>', html)


if __name__ == '__main__':
    unittest.main() 