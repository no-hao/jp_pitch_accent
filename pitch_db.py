import json
import os

PITCH_DB_PATH = os.path.join(os.path.dirname(__file__), 'pitch_db.json')

class PitchDB:
    def __init__(self, db_path=PITCH_DB_PATH):
        with open(db_path, encoding='utf-8') as f:
            self.db = json.load(f)

    def lookup(self, dict_form):
        """Return pitch info for a given dictionary form, or None if not found."""
        return self.db.get(dict_form)
