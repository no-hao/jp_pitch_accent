from pitch_db import PitchDB, PITCH_TYPE_LABELS

def test_pitch_db():
    """Test PitchDB functionality with SudachiPy"""
    print("\nTesting PitchDB...")
    
    # Create a new PitchDB instance
    db = PitchDB()
    
    # Test words
    test_words = [
        '大学',
        '食べる',
        '行きます',
        '見る',
        '日本語',
        '勉強する'
    ]
    
    for word in test_words:
        print(f"\nAnalyzing word: {word}")
        
        # Try cache first
        print("Checking cache...")
        result = db.lookup(word)
        if result:
            print(f"Found in cache: {result}")
            continue
            
        print("Not in cache, analyzing with SudachiPy...")
        result = db.lookup_with_cache(word)
        if result:
            print(f"Analysis successful!")
            print(f"Reading: {result['reading']}")
            print(f"Drop position: {result['drop_pos']}")
            print(f"Number of morae: {result['num_mora']}")
            pitch_type_label = result.get('pitch_type_label', PITCH_TYPE_LABELS[result['pitch_type']])
            print(f"Pitch type: {result['pitch_type']} ({pitch_type_label})")
        else:
            print("Analysis failed!")

if __name__ == '__main__':
    test_pitch_db() 