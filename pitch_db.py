import json
import os
import requests
from bs4 import BeautifulSoup
from sudachipy import tokenizer
from sudachipy import dictionary

PITCH_DB_PATH = os.path.join(os.path.dirname(__file__), "pitch_db.json")

# Map drop position to type
# 0: Heiban, 1: Atamadaka, n==num_mora: Odaka, else Nakadaka
PITCH_TYPE_LABELS = {
    0: "Heiban",
    1: "Atamadaka",
    2: "Nakadaka",
    3: "Odaka"
}

def drop_pos_to_type(drop_pos: int, num_mora: int) -> int:
    """
    Determines pitch accent type based on drop position.
    - 0: Heiban (no drop)
    - 1: Atamadaka (drops after first)
    - num_mora: Odaka (drops after last)
    - else: Nakadaka (drops after some middle mora)
    """
    if drop_pos == 0:
        return 0  # Heiban
    elif drop_pos == 1:
        return 1  # Atamadaka
    elif drop_pos == num_mora:
        return 3  # Odaka
    else:
        return 2  # Nakadaka

class PitchDB:
    """
    Handles pitch accent lookup, caching, OJAD queries, and fallback reading analysis.
    """

    def __init__(self, db_path: str = PITCH_DB_PATH):
        self.db_path: str = db_path
        if os.path.exists(db_path):
            with open(db_path, encoding="utf-8") as f:
                self.db = json.load(f)
        else:
            self.db = {}
            self.save()
        self.tokenizer = dictionary.Dictionary().create()
        self.mode = tokenizer.Tokenizer.SplitMode.C

    def lookup(self, dict_form: str):
        """
        Look up a dictionary form in cache.
        """
        print(f"Looking up {dict_form} in cache...")
        result = self.db.get(dict_form)
        print(f"Cache result: {result}")
        return result

    def add_entry(
        self,
        dict_form: str,
        reading: str,
        drop_pos: int,
        num_mora: int,
        pitch_type: int,
        meaning: str = None
    ):
        """
        Add a new entry to the local pitch accent database and save it.
        """
        print(f"Adding entry to cache: {dict_form} = {reading} (drop_pos {drop_pos}, type {pitch_type})")
        self.db[dict_form] = {
            "reading": reading,
            "drop_pos": drop_pos,
            "num_mora": num_mora,
            "pitch_type": pitch_type,
            "meaning": meaning
        }
        self.save()

    def save(self):
        """
        Save the pitch accent database to disk.
        """
        print(f"Saving cache to {self.db_path}")
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)

    def fetch_from_ojad(self, dict_form: str):
        """
        Fetch pitch accent info for a word (in dictionary form) from OJAD.
        Returns (reading, drop_pos, num_mora, pitch_type) or None on failure.
        """
        print(f"Fetching {dict_form} from OJAD...")
        url = "http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/word:"
        try:
            target_url = url + dict_form
            print(f"Making request to {target_url}")
            resp = requests.get(target_url, timeout=10)
            resp.raise_for_status()
            print("Got response from OJAD")
            soup = BeautifulSoup(resp.text, "html.parser")
            print("Parsed HTML response")

            # Find the OJAD results row for the word (first occurrence most reliable for plain forms)
            word_row = soup.find("tr", id=lambda x: x and x.startswith("word_"))
            print(f"Found word row: {word_row is not None}")
            if not word_row:
                print("No word row found")
                return None

            accented_word = word_row.find("span", class_="accented_word")
            if not accented_word:
                print("No accented word found")
                return None

            # Reading: collect text from all mora-character spans
            reading = "".join(span.text for span in accented_word.find_all("span", class_="char"))
            reading = reading.strip()
            print(f"Got reading: {reading}")

            # Find all mora spans (look for spans with mola_ class)
            mora_spans = accented_word.find_all("span", class_=lambda x: x and "mola_" in x)
            num_mora = len(mora_spans)
            drop_pos = 0  # Default to Heiban

            # Check each mora span for accent_top class
            for idx, mora in enumerate(mora_spans):
                classes = mora.get("class", [])
                print(f"  Mora {idx+1}: classes={classes}")
                if "accent_top" in classes:
                    drop_pos = idx + 1  # accent_top is on k-th mora, drop is after k-th mora (1-based)
                    print(f"  Found accent_top at mora {idx+1}, drop_pos set to {drop_pos}")
                    break

            print(f"Num mora: {num_mora}, Drop pos: {drop_pos}")
            pitch_type = drop_pos_to_type(drop_pos, num_mora)
            print(f"Determined pitch type: {pitch_type} ({PITCH_TYPE_LABELS[pitch_type]})")
            return reading, drop_pos, num_mora, pitch_type
        except Exception as e:
            print(f"OJAD fetch failed for {dict_form}: {e}")
            print(f"Exception type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
        return None

    def analyze_word(self, word: str):
        """
        Uses SudachiPy to analyze a word, returning dict with keys:
        - surface
        - dict_form
        - reading
        - pos
        or None if analysis failed.
        """
        tokens = self.tokenizer.tokenize(word, self.mode)
        if not tokens:
            return None
        token = tokens[0]
        return {
            "surface": token.surface(),
            "dict_form": token.dictionary_form(),
            "reading": token.reading_form(),
            "pos": token.part_of_speech()
        }

    def lookup_with_cache(self, word: str):
        """
        Looks up a word for pitch accent info, first in cache, then OJAD, then fallback to reading.
        Returns a dict of pitch info.
        """
        print(f"\nLooking up {word} with cache...")
        analysis = self.analyze_word(word)
        if not analysis:
            print("Failed to analyze word with SudachiPy")
            return None

        dict_form = analysis["dict_form"]
        print(f"Dictionary form: {dict_form}")
        result = self.lookup(dict_form)
        if result is not None:
            print("Found in cache")
            return result

        print("Not in cache, trying OJAD...")
        ojad_result = self.fetch_from_ojad(dict_form)
        if ojad_result:
            print("Got result from OJAD")
            reading, drop_pos, num_mora, pitch_type = ojad_result
            self.add_entry(dict_form, reading, drop_pos, num_mora, pitch_type)
            return {
                "reading": reading,
                "drop_pos": drop_pos,
                "num_mora": num_mora,
                "pitch_type": pitch_type,
                "pitch_type_label": PITCH_TYPE_LABELS[pitch_type]
            }

        print("OJAD failed, using SudachiPy reading with default pitch")
        reading = analysis["reading"]
        drop_pos = 0
        num_mora = len(reading)
        pitch_type = 0
        self.add_entry(dict_form, reading, drop_pos, num_mora, pitch_type)
        return {
            "reading": reading,
            "drop_pos": drop_pos,
            "num_mora": num_mora,
            "pitch_type": pitch_type,
            "pitch_type_label": PITCH_TYPE_LABELS[pitch_type]
        }
