import json
import os
import requests
from bs4 import BeautifulSoup

PITCH_DB_PATH = os.path.join(os.path.dirname(__file__), 'pitch_db.json')

class PitchDB:
    def __init__(self, db_path=PITCH_DB_PATH):
        self.db_path = db_path
        with open(db_path, encoding='utf-8') as f:
            self.db = json.load(f)

    def lookup(self, dict_form):
        """Return pitch info for a given dictionary form, or None if not found."""
        return self.db.get(dict_form)

    def add_entry(self, dict_form, reading, pitch):
        self.db[dict_form] = {"reading": reading, "pitch": pitch}
        self.save()

    def save(self):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)

    def fetch_from_ojad(self, dict_form):
        """
        Try to fetch pitch accent info from OJAD for a given dictionary form.
        Returns (reading, pitch) if found, else None.
        """
        url = f"https://www.gavo.t.u-tokyo.ac.jp/ojad/phrasing/index"
        params = {"word": dict_form, "accent": "1"}
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            # OJAD's HTML is complex; this is a minimal example for verbs/nouns
            # Look for the pitch number in the table (simplified for demo)
            pitch_cell = soup.find('td', class_='accent')
            reading_cell = soup.find('td', class_='reading')
            if pitch_cell and reading_cell:
                pitch = int(pitch_cell.text.strip())
                reading = reading_cell.text.strip()
                return reading, pitch
        except Exception as e:
            print(f"OJAD fetch failed for {dict_form}: {e}")
        return None

    def lookup_with_cache(self, dict_form):
        """
        Lookup pitch info, and if missing, try to fetch from OJAD and cache it.
        """
        result = self.lookup(dict_form)
        if result is not None:
            return result
        fetched = self.fetch_from_ojad(dict_form)
        if fetched:
            reading, pitch = fetched
            self.add_entry(dict_form, reading, pitch)
            return {"reading": reading, "pitch": pitch}
        return None
