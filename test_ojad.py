from pitch_db import PitchDB, PITCH_TYPE_LABELS
import requests
from bs4 import BeautifulSoup

# Chart-based test cases: (word, expected_drop_pos, expected_type_label)
test_cases = [
    # Heiban (0)
    ("名", 0, "Heiban"),
    ("水", 0, "Heiban"),
    ("会社", 0, "Heiban"),
    ("大学", 0, "Heiban"),
    ("中国語", 0, "Heiban"),
    ("見物", 0, "Heiban"),
    # Atamadaka (1)
    ("木", 1, "Atamadaka"),
    ("秋", 1, "Atamadaka"),
    ("電気", 1, "Atamadaka"),
    ("文学", 1, "Atamadaka"),
    ("シャーベット", 1, "Atamadaka"),
    ("けんもほろろ", 1, "Atamadaka"),
    # Nakadaka (2, 3, ...)
    ("花", 2, "Nakadaka"),
    ("お菓子", 2, "Nakadaka"),
    ("雪国", 2, "Nakadaka"),
    ("普及率", 2, "Nakadaka"),
    ("お巡りさん", 2, "Nakadaka"),
    ("金婚式", 2, "Nakadaka"),
    ("国語辞典", 2, "Nakadaka"),
    # Odaka (drop after last mora)
    ("男", 3, "Odaka"),
    ("弟", 4, "Odaka"),
    ("桃の花", 5, "Odaka"),
]

def test_ojad_chart_examples():
    print("\nTesting OJAD with chart-based examples...")
    db = PitchDB()
    for word, expected_drop, expected_type in test_cases:
        print(f"\nWord: {word}")
        result = db.lookup_with_cache(word)
        if result:
            print(f"  Reading: {result['reading']}")
            print(f"  Drop pos: {result['drop_pos']} (expected: {expected_drop})")
            print(f"  Mora count: {result['num_mora']}")
            # Handle both cached and fresh results
            pitch_type_label = result.get('pitch_type_label', PITCH_TYPE_LABELS[result['pitch_type']])
            print(f"  Type: {pitch_type_label} (expected: {expected_type})")
        else:
            print("  Failed to get info")

# def print_ojad_html_chunk(word):
#     url = "http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/word:" + word
#     resp = requests.get(url, timeout=10)
#     soup = BeautifulSoup(resp.text, 'html.parser')
#     word_row = soup.find('tr', id=lambda x: x and x.startswith('word_'))
#     if word_row:
#         print(f"\n--- OJAD HTML for {word} ---")
#         print(word_row.prettify())
#     else:
#         print(f"\n--- No word row found for {word} ---")
#
# def main():
#     for word in ["橋", "花"]:
#         print_ojad_html_chunk(word)

if __name__ == '__main__':
    test_ojad_chart_examples()
    # main() 