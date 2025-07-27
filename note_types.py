from aqt import mw
from anki.models import ModelManager
import json
import os

DEFAULT_MODEL_NAME = "Japanese with Pitch Accent"

def setup_note_types():
    """Set up the note types for pitch accent display"""
    if not mw.col:
        print("Collection not loaded")
        return None
        
    mm = mw.col.models
    
    # Check if our note type already exists
    model = mm.by_name(DEFAULT_MODEL_NAME)
    if not model:
        # Create it
        model = mm.new(DEFAULT_MODEL_NAME)
        
        # Add fields
        mm.add_field(model, mm.new_field("Expression"))
        mm.add_field(model, mm.new_field("Reading"))
        mm.add_field(model, mm.new_field("Meaning"))
        
        # Add card templates
        t = mm.new_template("Recognition")
        t['qfmt'] = '''
<div class="expression">{{Expression}}</div>
'''
        t['afmt'] = '''
{{FrontSide}}
<hr id="answer">
<div class="reading">{{Reading}}</div>
<div class="meaning">{{Meaning}}</div>
'''
        mm.add_template(model, t)
        
        # Add CSS
        model['css'] = '''
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}

.expression {
    font-size: 30px;
}

.reading {
    font-size: 24px;
    color: #666;
}

.meaning {
    font-size: 20px;
    color: #333;
    margin-top: 20px;
}
'''
        
        # Save model
        mm.add(model)
        print(f"Created note type: {model['name']}")
    else:
        print(f"Note type already exists: {model['name']}")
        
    return model 