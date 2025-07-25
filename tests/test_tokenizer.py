# tests/test_tokenizer.py

import unittest
from typing import List, Dict
from pitch_tokenizer import JapaneseTokenizer


def is_katakana_word(word: str) -> bool:
    """Return True if the word is entirely katakana, allowing the prolonged sound mark (ー)."""
    return all(
        ('ァ' <= c <= 'ヴ') or c == 'ー'
        for c in word
    )


class TestJapaneseTokenizer(unittest.TestCase):
    def setUp(self) -> None:
        # Initialize tokenizer instance before each test
        self.tokenizer = JapaneseTokenizer()

    def test_basic_sentence(self) -> None:
        sentence: str = "今日はいい天気ですね。"
        tokens: List[Dict[str, str]] = self.tokenizer.tokenize(sentence)
        self.assertGreater(len(tokens), 0)
        self.assertEqual(tokens[0]["surface"], "今日")
        self.assertEqual(tokens[0]["pos"], "名詞")
        self.assertEqual(tokens[0]["reading"], "キョウ")

    def test_proper_noun_name(self) -> None:
        sentence: str = "山田太郎は学生です。"
        tokens: List[Dict[str, str]] = self.tokenizer.tokenize(sentence)
        name_tokens: List[Dict[str, str]] = [
            t for t in tokens if t["surface"] in ["山田", "太郎"]
        ]
        self.assertEqual(len(name_tokens), 2)
        for t in name_tokens:
            self.assertIn("名詞", t["pos"])

    def test_punctuation_and_numbers(self) -> None:
        sentence: str = "今日は2023年7月24日です。"
        tokens: List[Dict[str, str]] = self.tokenizer.tokenize(sentence)
        surfaces: List[str] = [t["surface"] for t in tokens]
        self.assertIn("2023", surfaces)
        self.assertIn("年", surfaces)
        self.assertIn("。", surfaces)

    def test_foreign_words(self) -> None:
        sentence: str = "コンピュータとインターネットは便利です。"
        tokens: List[Dict[str, str]] = self.tokenizer.tokenize(sentence)
        katakana_tokens: List[Dict[str, str]] = [
            t for t in tokens if is_katakana_word(t["surface"])
        ]
        self.assertGreaterEqual(len(katakana_tokens), 2)
        for t in katakana_tokens:
            self.assertEqual(t["pos"], "名詞")

    def test_conjugated_verb(self) -> None:
        sentence: str = "読んでいる本は面白いです。"
        tokens: List[Dict[str, str]] = self.tokenizer.tokenize(sentence)
        yomutokens: List[Dict[str, str]] = [t for t in tokens if t["dict"] == "読む"]
        self.assertGreater(len(yomutokens), 0)
        for token in yomutokens:
            self.assertIn("読む", token["dict"])
            self.assertIn("動詞", token["pos"])

    def test_adjective_tokenization(self) -> None:
        sentence: str = "この映画は面白い。"
        tokens: List[Dict[str, str]] = self.tokenizer.tokenize(sentence)
        adj_tokens: List[Dict[str, str]] = [t for t in tokens if "形容詞" in t["pos"]]
        self.assertGreater(len(adj_tokens), 0)
        for t in adj_tokens:
            self.assertTrue(len(t["reading"]) > 0)


if __name__ == "__main__":
    unittest.main()

