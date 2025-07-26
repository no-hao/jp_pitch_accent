from pitch_tokenizer import JapaneseTokenizer

def test_tokenization():
    """Test Japanese text tokenization with SudachiPy"""
    print("\nTesting tokenization...")
    
    tokenizer = JapaneseTokenizer()
    
    # Test sentences
    test_texts = [
        '大学に行きます。',
        '私は日本語を勉強しています。',
        '食べる',
        '見る'
    ]
    
    for text in test_texts:
        print(f"\nTokenizing: {text}")
        tokens = tokenizer.tokenize(text)
        
        for token in tokens:
            print(f"\nToken:")
            print(f"  Surface:   {token['surface']}")
            print(f"  Dict form: {token['dict_form']}")
            print(f"  Reading:   {token['reading']}")
            print(f"  POS:       {token['pos']}")

if __name__ == '__main__':
    test_tokenization() 