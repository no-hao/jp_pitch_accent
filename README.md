# Japanese Pitch Accent Anki Addon

An Anki addon that automatically adds Japanese pitch accent information to vocabulary cards.

## Features

- **Automatic pitch accent lookup** when editing cards
- **Integration with OJAD** (Online Japanese Accent Dictionary) for missing entries
- **SVG pitch accent visualization** 
- **Custom note type** with Expression, Reading, and Pitch fields
- **Tokenization** of Japanese text to process individual words

## Installation

1. Clone this repository to your Anki addons directory:
   ```
   git clone <repository-url> /path/to/anki/addons21/jp_pitch_accent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Restart Anki

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
- `tests/test_tokenizer.py` - Tests for Japanese text tokenization
- `tests/test_ojad.py` - Tests for OJAD integration
- `tests/test_pitch_svg.py` - Tests for SVG generation
- `tests/test_svg_generation.py` - Tests for SVG generation workflow
- `tests/test_anki_integration.py` - Tests for Anki integration
- `tests/test_mvp_integration.py` - Tests for MVP functionality

### Project Structure

```
jp_pitch_accent/
├── __init__.py              # Main addon entry point
├── pitch_db.py              # Pitch accent database
├── pitch_svg.py             # SVG generation
├── pitch_tokenizer.py       # Japanese text tokenization
├── note_types.py            # Anki note type setup
├── pipeline.py              # Main processing pipeline
├── config.json              # Configuration
├── pitch_db.json            # Pitch accent data
├── tests/                   # Test directory
│   ├── __init__.py
│   ├── test_pitch_db.py
│   ├── test_tokenizer.py
│   ├── test_ojad.py
│   ├── test_pitch_svg.py
│   ├── test_svg_generation.py
│   ├── test_anki_integration.py
│   └── test_mvp_integration.py
├── run_tests.py             # Test runner
├── pytest.ini              # Pytest configuration
├── setup.py                # Package setup
└── requirements.txt        # Dependencies
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