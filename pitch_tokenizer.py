from sudachipy import tokenizer
from sudachipy import dictionary

class JapaneseTokenizer:
    def __init__(self):
        self.tokenizer = dictionary.Dictionary().create()
        
    def katakana_to_hiragana(self, text):
        """Convert katakana to hiragana with comprehensive mapping."""
        # Comprehensive katakana to hiragana mapping
        katakana_to_hiragana_map = {
            # Basic katakana
            'ァ': 'ぁ', 'ア': 'あ', 'ィ': 'ぃ', 'イ': 'い', 'ゥ': 'ぅ', 'ウ': 'う', 'ェ': 'ぇ', 'エ': 'え', 'ォ': 'ぉ', 'オ': 'お',
            'カ': 'か', 'ガ': 'が', 'キ': 'き', 'ギ': 'ぎ', 'ク': 'く', 'グ': 'ぐ', 'ケ': 'け', 'ゲ': 'げ', 'コ': 'こ', 'ゴ': 'ご',
            'サ': 'さ', 'ザ': 'ざ', 'シ': 'し', 'ジ': 'じ', 'ス': 'す', 'ズ': 'ず', 'セ': 'せ', 'ゼ': 'ぜ', 'ソ': 'そ', 'ゾ': 'ぞ',
            'タ': 'た', 'ダ': 'だ', 'チ': 'ち', 'ヂ': 'ぢ', 'ッ': 'っ', 'ツ': 'つ', 'ヅ': 'づ', 'テ': 'て', 'デ': 'で', 'ト': 'と', 'ド': 'ど',
            'ナ': 'な', 'ニ': 'に', 'ヌ': 'ぬ', 'ネ': 'ね', 'ノ': 'の',
            'ハ': 'は', 'バ': 'ば', 'パ': 'ぱ', 'ヒ': 'ひ', 'ビ': 'び', 'ピ': 'ぴ', 'フ': 'ふ', 'ブ': 'ぶ', 'プ': 'ぷ', 'ヘ': 'へ', 'ベ': 'べ', 'ペ': 'ぺ', 'ホ': 'ほ', 'ボ': 'ぼ', 'ポ': 'ぽ',
            'マ': 'ま', 'ミ': 'み', 'ム': 'む', 'メ': 'め', 'モ': 'も',
            'ャ': 'ゃ', 'ヤ': 'や', 'ュ': 'ゅ', 'ユ': 'ゆ', 'ョ': 'ょ', 'ヨ': 'よ',
            'ラ': 'ら', 'リ': 'り', 'ル': 'る', 'レ': 'れ', 'ロ': 'ろ',
            'ワ': 'わ', 'ヲ': 'を', 'ン': 'ん',
            # Extended katakana
            'ヴ': 'ゔ', 'ヵ': 'ゕ', 'ヶ': 'ゖ',
            # Small katakana
            'ァ': 'ぁ', 'ィ': 'ぃ', 'ゥ': 'ぅ', 'ェ': 'ぇ', 'ォ': 'ぉ',
            'ャ': 'ゃ', 'ュ': 'ゅ', 'ョ': 'ょ',
            'ッ': 'っ',
            # Prolonged sound mark
            'ー': 'ー'  # Keep as is
        }
        
        # Convert using the mapping
        result = ''
        for char in text:
            result += katakana_to_hiragana_map.get(char, char)
        
        return result
        
    def tokenize(self, text):
        """
        Tokenize Japanese text using SudachiPy.
        Returns a list of dictionaries with surface form and dictionary form.
        """
        tokens = []
        mode = tokenizer.Tokenizer.SplitMode.C  # Use mode C for most granular tokenization
        
        for token in self.tokenizer.tokenize(text, mode):
            # Convert katakana reading to hiragana
            reading = self.katakana_to_hiragana(token.reading_form())
            
            tokens.append({
                'surface': token.surface(),  # Surface form (as written)
                'dict_form': token.dictionary_form(),  # Dictionary form
                'reading': reading,  # Reading in hiragana
                'pos': token.part_of_speech()  # Part of speech info
            })
            
        return tokens
        
    def is_kanji(self, char):
        """Check if a character is a kanji."""
        return 0x4E00 <= ord(char) <= 0x9FFF
        
    def is_kana(self, char):
        """Check if a character is hiragana or katakana."""
        return (0x3040 <= ord(char) <= 0x309F) or (0x30A0 <= ord(char) <= 0x30FF)
