from sudachipy import tokenizer
from sudachipy import dictionary

class JapaneseTokenizer:
    def __init__(self):
        self.tokenizer = dictionary.Dictionary().create()
        
    def tokenize(self, text):
        """
        Tokenize Japanese text using SudachiPy.
        Returns a list of dictionaries with surface form and dictionary form.
        """
        tokens = []
        mode = tokenizer.Tokenizer.SplitMode.C  # Use mode C for most granular tokenization
        
        for token in self.tokenizer.tokenize(text, mode):
            tokens.append({
                'surface': token.surface(),  # Surface form (as written)
                'dict_form': token.dictionary_form(),  # Dictionary form
                'reading': token.reading_form(),  # Reading in katakana
                'pos': token.part_of_speech()  # Part of speech info
            })
            
        return tokens
        
    def is_kanji(self, char):
        """Check if a character is a kanji."""
        return 0x4E00 <= ord(char) <= 0x9FFF
        
    def is_kana(self, char):
        """Check if a character is hiragana or katakana."""
        return (0x3040 <= ord(char) <= 0x309F) or (0x30A0 <= ord(char) <= 0x30FF)
