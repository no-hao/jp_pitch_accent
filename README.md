# Japanese Pitch Accent Anki Addon

An Anki addon that automatically adds Japanese pitch accent information to vocabulary cards.

## Features

- **Automatic pitch accent lookup** when editing cards
- **Integration with OJAD** (Online Japanese Accent Dictionary) for missing entries
- **SVG pitch accent visualization** 
- **Custom note type** with Expression, Reading, and Meaning fields
- **Tokenization** of Japanese text to process individual words

## Installation

1. Clone this repository to your Anki addons directory:
   ```
   git clone <repository-url> /path/to/anki/addons21/jp_pitch_accent
   ```

2. Install dependencies in Anki's Python environment:
   ```bash
   # Run the installation script
   python install_dependencies.py
   
   # Or manually install in Anki's environment
   "/Users/ericstine/Library/Application Support/AnkiProgramFiles/.venv/bin/pip" install -r requirements.txt
   ```

3. Restart Anki

**Note:** This addon requires dependencies to be installed in Anki's Python environment, not your system Python. The installation script handles this automatically.

## Development

### Running Tests

The project uses unittest framework for testing. All tests are located in the `tests/` directory.

#### Run all tests:
```bash
python run_tests.py
```

#### Run tests with pytest:
```bash
pytest
```

#### Run specific test file:
```bash
python -m pytest tests/test_pitch_db.py
```

#### Run tests with coverage:
```bash
pytest --cov=. tests/
```

### Test Structure

- `tests/test_pitch_db.py` - Tests for pitch database functionality
- `tests/test_sentence_processor.py` - Tests for sentence-level pitch processing
- `tests/test_pitch_svg.py` - Tests for SVG generation
- `tests/test_svg_generation.py` - Tests for SVG generation workflow
- `tests/test_anki_integration.py` - Tests for Anki integration
- `tests/test_mvp_integration.py` - Tests for MVP functionality
- `tests/test_field_auto_fill.py` - Tests for field auto-fill functionality
- `tests/test_ojad.py` - Tests for OJAD integration
- `tests/test_tokenizer.py` - Tests for Japanese text tokenization
- `tests/test_chart_comparison.py` - Tests for chart-based validation

### Project Structure

```
jp_pitch_accent/
├── __init__.py                    # Main addon entry point
├── sentence_pitch_processor.py    # Sentence-level pitch accent processing
├── pitch_db.py                    # Pitch accent database and OJAD integration
├── pitch_svg.py                   # SVG generation for pitch accent visualization
├── utils.py                       # Shared utility functions
├── note_types.py                  # Anki note type setup
├── config.json                    # Addon configuration
├── pitch_db.json                  # Pitch accent data cache
├── manifest.json                  # Addon metadata
├── tests/                         # Test directory
│   ├── __init__.py
│   ├── test_pitch_db.py
│   ├── test_sentence_processor.py
│   ├── test_pitch_svg.py
│   ├── test_svg_generation.py
│   ├── test_anki_integration.py
│   ├── test_mvp_integration.py
│   ├── test_field_auto_fill.py
│   ├── test_ojad.py
│   ├── test_tokenizer.py
│   └── test_chart_comparison.py
├── run_tests.py                   # Test runner
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Dependencies
├── venv/                         # Virtual environment
├── README.md                    # Documentation
├── LICENSE                      # License
└── .gitignore                  # Git ignore rules
```

## Configuration

Edit `config.json` to customize the addon behavior:

```json
{
    "enabled": true,
    "show_on_front": true,
    "show_on_back": true,
    "pitch_field_name": "Pitch",
    "word_field_name": "Expression",
    "reading_field_name": "Reading",
    "ojad": {
        "enabled": true,
        "rate_limit": 5,
        "timeout": 10
    },
    "style": {
        "svg_scale": 1.0,
        "display_type": "popup",
        "popup_trigger": "hover",
        "indicator_style": "dotted_underline"
    }
}
```

## License

MIT License - see LICENSE file for details.