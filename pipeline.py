from pitch_tokenizer import JapaneseTokenizer
from pitch_db import PitchDB
from html_renderer import render_ruby

def annotate_pitch(sentence):
    """
    Tokenize a Japanese sentence, look up pitch accent info, and render annotated HTML.
    """
    tokenizer = JapaneseTokenizer()
    db = PitchDB()
    tokens = tokenizer.tokenize(sentence)
    annotated_tokens = []
    for token in tokens:
        pitch_info = db.lookup(token["dict"])
        if pitch_info:
            annotated_tokens.append({
                "surface": token["surface"],
                "reading": pitch_info["reading"],
                "pitch": pitch_info["pitch"]
            })
        else:
            annotated_tokens.append({
                "surface": token["surface"],
                "reading": token["reading"],
                "pitch": None
            })
    return render_ruby(annotated_tokens) 