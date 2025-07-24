from sudachipy import tokenizer, dictionary


class JapaneseTokenizer:
    def __init__(self, mode=tokenizer.Tokenizer.SplitMode.B):
        self.tok = dictionary.Dictionary().create()
        self.mode = mode

    def tokenize(self, text):
        return [
            {
                "surface": m.surface(),
                "reading": m.reading_form(),
                "dict": m.dictionary_form(),
                "pos": m.part_of_speech()[0],
            }
            for m in self.tok.tokenize(text, self.mode)
        ]
