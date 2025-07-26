from aqt import mw, gui_hooks
from aqt.utils import showInfo
from aqt.editor import Editor
from anki.hooks import wrap, addHook
import json
import os

from . import pitch_svg
from . import pitch_db
from . import note_types
from . import pitch_tokenizer

def load_config():
    """Load addon configuration"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, encoding='utf-8') as f:
        return json.load(f)

def on_focus_lost(flag, note, field_idx):
    """Process field content when focus is lost"""
    # Only process if we're in our note type
    if not note or note.model()['name'] != note_types.DEFAULT_MODEL_NAME:
        return flag
        
    # Get field names
    field_names = mw.col.models.field_names(note.model())
    
    # Only process Expression field
    if field_names[field_idx] != 'Expression':
        return flag
        
    try:
        # Get the text
        text = note['Expression']
        print(f"Processing text: {text}")
        
        # Process the text
        tokenizer = pitch_tokenizer.JapaneseTokenizer()
        tokens = tokenizer.tokenize(text)
        print(f"Tokens: {tokens}")
        
        readings = []
        
        for token in tokens:
            surface = token["surface"]
            dict_form = token.get("dict", surface)
            
            # Skip processing for punctuation
            if all(not tokenizer.is_kanji(c) and not tokenizer.is_kana(c) for c in surface):
                continue
                
            # Get reading and pitch info
            pitch_info = db.lookup(dict_form)
            if not pitch_info and config['ojad']['enabled']:
                print(f"No pitch info found, trying OJAD for {dict_form}")
                pitch_info = db.lookup_with_cache(dict_form)
                
            if pitch_info:
                print(f"Found pitch info: {pitch_info}")
                reading = pitch_info["reading"]
                readings.append(reading)
        
        # Update Reading field
        if readings:
            note['Reading'] = ' '.join(readings)
            return True
            
        return flag
        
    except Exception as e:
        print(f"Error processing field: {e}")
        return flag

def init_pitch_accent():
    """Initialize the pitch accent addon"""
    global config, db
    
    print("Initializing pitch accent addon...")
    
    try:
        # Load configuration
        config = load_config()
        print("Config loaded successfully")
        
        # Initialize the pitch accent database
        db = pitch_db.PitchDB()
        print("Database initialized successfully")
        
        # Set up note types
        model = note_types.setup_note_types()
        if model:
            print(f"Note type setup complete: {model['name']}")
            print(f"Fields: {[f['name'] for f in model['flds']]}")
            print(f"Templates: {[t['name'] for t in model['tmpls']]}")
        else:
            print("Note type setup failed!")
            
        # Register our hooks
        addHook('editFocusLost', on_focus_lost)
        print("Hooks registered successfully")
        
        # For testing, show that we loaded
        showInfo("Pitch Accent addon loaded successfully!")
        
    except Exception as e:
        print(f"Error during initialization: {e}")
        showInfo(f"Error loading Pitch Accent addon: {e}")

# Wait for profile to load before initializing
gui_hooks.profile_did_open.append(init_pitch_accent) 