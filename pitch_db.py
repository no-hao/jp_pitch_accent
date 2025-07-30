import json
import os
import requests
from bs4 import BeautifulSoup
from sudachipy import tokenizer
from sudachipy import dictionary
from utils import katakana_to_hiragana

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
        if result and result.get("reading"):
            # Ensure reading is in hiragana
            result["reading"] = katakana_to_hiragana(result["reading"])
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
        # Ensure reading is in hiragana
        reading = katakana_to_hiragana(reading)
        
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

            # Find the OJAD results row for the word
            word_row = soup.find("tr", id=lambda x: x and x.startswith("word_"))
            print(f"Found word row: {word_row is not None}")
            if not word_row:
                print("No word row found")
                return None

            # Get all readings from the row
            all_readings = self._extract_all_readings_from_ojad_row(word_row)
            print(f"Found readings: {all_readings}")
            
            # Find the specific reading that matches our search
            target_reading = self._find_matching_reading(dict_form, all_readings)
            if not target_reading:
                print(f"No matching reading found for {dict_form}")
                return None
            
            print(f"Using reading: {target_reading['reading']}")
            
            # Extract pitch pattern for this specific reading
            reading = target_reading['reading']
            mora_spans = target_reading['mora_spans']
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
    
    def _extract_all_readings_from_ojad_row(self, word_row):
        """
        Extract all readings and their mora spans from an OJAD word row.
        Returns list of dicts with 'reading' and 'mora_spans' keys.
        """
        readings = []
        
        # Find all accented word spans
        accented_words = word_row.find_all("span", class_="accented_word")
        
        for accented_word in accented_words:
            # Get the reading text
            reading = "".join(span.text for span in accented_word.find_all("span", class_="char"))
            reading = reading.strip()
            
            # Get mora spans for this reading
            mora_spans = accented_word.find_all("span", class_=lambda x: x and "mola_" in x)
            
            if reading and mora_spans:
                readings.append({
                    'reading': reading,
                    'mora_spans': mora_spans
                })
        
        return readings
    
    def _find_matching_reading(self, search_word, all_readings):
        """
        Find the reading that best matches the search word.
        For conjugated forms, we need to find the specific conjugation.
        """
        # First, try exact match
        for reading_data in all_readings:
            if reading_data['reading'] == search_word:
                return reading_data
        
        # If no exact match, try to find the conjugated form
        # Look for the specific conjugation that matches what we're searching for
        for reading_data in all_readings:
            reading = reading_data['reading']
            
            # Check if this reading matches the search word's reading
            # For example, if searching for "買います", look for "かいます"
            if reading == search_word:
                return reading_data
            
            # Also check if the reading is contained in the search word's reading
            # This handles cases where the search word might be in a different format
            if len(reading) > 2 and search_word.endswith(reading):
                return reading_data
        
        # If still no match, try to find the most similar reading
        # This is a fallback for cases where exact matching fails
        for reading_data in all_readings:
            reading = reading_data['reading']
            # Check for partial matches
            if any(char in reading for char in search_word) or any(char in search_word for char in reading):
                return reading_data
        
        # If still no match, return the first reading (fallback)
        if all_readings:
            return all_readings[0]
        
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
        reading = analysis["reading"]  # Get the actual reading from tokenization
        print(f"Dictionary form: {dict_form}")
        print(f"Reading: {reading}")
        
        # Convert Katakana reading to Hiragana for OJAD matching
        hiragana_reading = katakana_to_hiragana(reading)
        print(f"Hiragana reading: {hiragana_reading}")
        
        # First, check cache
        result = self.lookup(dict_form)
        if result is not None:
            print("Found in cache")
            return result

        # Second, try OJAD with the hiragana reading
        print("Not in cache, trying OJAD...")
        ojad_result = self.fetch_from_ojad_with_reading(dict_form, hiragana_reading)
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

        # Third, fallback to SudachiPy reading (convert katakana to hiragana)
        print("OJAD failed, using SudachiPy reading with default pitch")
        reading = hiragana_reading
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
    
    def lookup_conjugated_form(self, conjugated_surface: str, conjugated_reading: str, dict_form: str):
        """
        Look up a conjugated form specifically.
        This is for cases where we have a conjugated form like '行きます' with reading 'いきます'.
        """
        print(f"\nLooking up conjugated form: {conjugated_surface} (reading: {conjugated_reading})")
        
        # Convert to hiragana
        hiragana_reading = katakana_to_hiragana(conjugated_reading)
        print(f"Hiragana reading: {hiragana_reading}")
        
        # Try OJAD with the conjugated reading
        ojad_result = self.fetch_from_ojad_with_reading(dict_form, hiragana_reading)
        if ojad_result:
            print("Got result from OJAD for conjugated form")
            reading, drop_pos, num_mora, pitch_type = ojad_result
            # Store with the conjugated surface as key
            self.add_entry(conjugated_surface, reading, drop_pos, num_mora, pitch_type)
            return {
                "reading": reading,
                "drop_pos": drop_pos,
                "num_mora": num_mora,
                "pitch_type": pitch_type,
                "pitch_type_label": PITCH_TYPE_LABELS[pitch_type]
            }
        
        # Fallback to normal lookup
        print("No conjugated form found, falling back to normal lookup")
        return self.lookup_with_cache(conjugated_surface)
    
    def fetch_from_ojad_with_reading(self, dict_form: str, target_reading: str):
        """
        Fetch pitch accent info from OJAD using the specific reading.
        This allows us to find the correct conjugated form.
        """
        print(f"Fetching {dict_form} (reading: {target_reading}) from OJAD...")
        url = "http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/word:"
        try:
            target_url = url + dict_form
            print(f"Making request to {target_url}")
            resp = requests.get(target_url, timeout=10)
            resp.raise_for_status()
            print("Got response from OJAD")
            soup = BeautifulSoup(resp.text, "html.parser")
            print("Parsed HTML response")

            # Find the OJAD results row for the word
            word_row = soup.find("tr", id=lambda x: x and x.startswith("word_"))
            print(f"Found word row: {word_row is not None}")
            if not word_row:
                print("No word row found")
                return None

            # Get all readings from the row
            all_readings = self._extract_all_readings_from_ojad_row(word_row)
            print(f"Found readings: {[r['reading'] for r in all_readings]}")
            
            # Find the specific reading that matches our target reading
            target_reading_data = self._find_matching_reading(target_reading, all_readings)
            if not target_reading_data:
                print(f"No matching reading found for {target_reading}")
                return None
            
            print(f"Using reading: {target_reading_data['reading']}")
            
            # Extract pitch pattern for this specific reading
            reading = target_reading_data['reading']
            mora_spans = target_reading_data['mora_spans']
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
