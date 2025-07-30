#!/usr/bin/env python3
"""
Sentence-level Japanese pitch accent processor.
Preserves individual word pitch patterns and connects them properly across word boundaries.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pitch_db import PitchDB, PITCH_TYPE_LABELS
from pitch_svg import get_pitch_pattern, get_accent_position
from sudachipy import tokenizer
from sudachipy import dictionary
from utils import katakana_to_hiragana

class SentencePitchProcessor:
    """
    Processes Japanese sentences to generate unified pitch accent patterns.
    Preserves individual word pitch patterns and connects them properly.
    """
    
    def __init__(self):
        self.db = PitchDB()
        self.tokenizer = dictionary.Dictionary().create()
        
        # Particles that typically form phrase boundaries
        self.boundary_particles = {
            'は', 'も'  # These typically create phrase boundaries
        }
        
        # Particles that attach to preceding words
        self.attaching_particles = {
            'が', 'を', 'に', 'で', 'へ', 'と', 'から', 'まで', 'より', 'まで'
        }
    
    def process_sentence(self, sentence: str) -> dict:
        """
        Process entire sentence and return unified pitch pattern.
        
        Args:
            sentence: Japanese sentence to process
            
        Returns:
            dict with unified pitch pattern, accent positions, and metadata
        """
        print(f"🎯 Processing sentence: {sentence}")
        
        # Step 1: Tokenize sentence
        tokens = self._tokenize(sentence)
        print(f"   Tokens: {[t['surface'] for t in tokens]}")
        
        # Step 2: Get pitch info for each token
        token_pitch_info = self._get_token_pitch_info(tokens)
        
        # Step 3: Detect phrase groups
        phrase_groups = self._detect_phrase_groups(token_pitch_info)
        
        # Step 4: Process each phrase group
        phrase_results = []
        for i, group in enumerate(phrase_groups):
            print(f"   Processing phrase group {i+1}: {[t['surface'] for t in group]}")
            phrase_result = self._process_phrase_group(group)
            phrase_results.append(phrase_result)
        
        # Step 5: Combine phrase results
        final_result = self._combine_phrase_results(phrase_results, sentence)
        
        return final_result
    
    def _tokenize(self, text):
        """
        Tokenize Japanese text using SudachiPy.
        Returns a list of dictionaries with surface form and dictionary form.
        """
        tokens = []
        mode = tokenizer.Tokenizer.SplitMode.C  # Use mode C for most granular tokenization
        
        for token in self.tokenizer.tokenize(text, mode):
            # Convert katakana reading to hiragana
            reading = katakana_to_hiragana(token.reading_form())
            
            tokens.append({
                'surface': token.surface(),  # Surface form (as written)
                'dict_form': token.dictionary_form(),  # Dictionary form
                'reading': reading,  # Reading in hiragana
                'pos': token.part_of_speech()  # Part of speech info
            })
            
        return tokens
    

    
    def _get_token_pitch_info(self, tokens: list) -> list:
        """
        Get pitch accent information for each token.
        Combines conjugated verb tokens to get full readings.
        """
        token_pitch_info = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            surface = token['surface']
            dict_form = token['dict_form']
            reading = token['reading']  # Use the actual reading from tokenization
            pos = token['pos']
            
            # Check if this is part of a conjugated verb
            combined_surface = surface
            combined_reading = reading
            combined_dict_form = dict_form
            
            # Look ahead to see if we have a conjugated verb
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                next_surface = next_token['surface']
                next_reading = next_token['reading']
                next_pos = next_token['pos']
                
                # Check if this forms a conjugated verb (verb + auxiliary/particle)
                if (pos[0] == '動詞' and 
                    next_pos[0] in ['助動詞', '助詞'] and
                    (next_pos[1] in ['接続助詞', '助動詞-タ', '助動詞-ナイ'] or 
                     next_pos[4] in ['助動詞-マス', '助動詞-タ', '助動詞-ナイ'])):
                    
                    # Combine the tokens
                    combined_surface = surface + next_surface
                    combined_reading = reading + next_reading
                    combined_dict_form = dict_form  # Keep the main verb's dict form
                    
                    # Skip the next token since we combined it
                    i += 1
            
            # Get pitch info from database using the combined form
            # For conjugated forms, we need to search with the combined reading
            if combined_surface != surface:
                # This is a conjugated form, search with the combined reading
                # Use the new conjugated form lookup method
                pitch_info = self.db.lookup_conjugated_form(combined_surface, combined_reading, combined_dict_form)
            else:
                # Single token, search normally
                pitch_info = self.db.lookup_with_cache(combined_surface)
            
            if pitch_info:
                # Use the actual reading from tokenization
                actual_reading = combined_reading if combined_reading else pitch_info['reading']
                
                # Normalize common reading variations
                if actual_reading == 'わたくし':
                    actual_reading = 'わたし'  # Use informal form
                
                token_pitch_info.append({
                    'surface': combined_surface,
                    'dict_form': combined_dict_form,
                    'reading': actual_reading,
                    'pitch_type': pitch_info['pitch_type'],
                    'drop_pos': pitch_info['drop_pos'],
                    'num_mora': len(actual_reading),  # Use actual reading length
                    'pos': pos,
                    'pitch_info': pitch_info
                })
            else:
                print(f"   {combined_surface}: No pitch info found")
                # Add with default Heiban pattern
                token_pitch_info.append({
                    'surface': combined_surface,
                    'dict_form': combined_dict_form,
                    'reading': combined_reading,
                    'pitch_type': 0,  # Heiban
                    'drop_pos': 0,
                    'num_mora': len(combined_reading),
                    'pos': pos,
                    'pitch_info': None
                })
            
            i += 1
        
        return token_pitch_info
    
    def _detect_phrase_groups(self, token_pitch_info: list) -> list:
        """
        Detect phrase boundaries and group tokens.
        Each group will be processed as a single phrase.
        """
        phrase_groups = []
        current_group = []
        
        for i, token in enumerate(token_pitch_info):
            surface = token['surface']
            pos = token['pos']
            
            # Check if this token starts a new phrase
            starts_new_phrase = False
            
            # Boundary particles start new phrases
            if surface in self.boundary_particles:
                starts_new_phrase = True
            
            # Pause indicators (comma, period) start new phrases
            elif surface in ['、', '。', '！', '？', '，', '．']:
                starts_new_phrase = True
            
            # Start new phrase if needed
            if starts_new_phrase and current_group:
                phrase_groups.append(current_group)
                current_group = []
            
            current_group.append(token)
        
        # Add final group
        if current_group:
            phrase_groups.append(current_group)
        
        print(f"   Detected {len(phrase_groups)} phrase groups")
        return phrase_groups
    
    def _process_phrase_group(self, group: list) -> dict:
        """
        Process a single phrase group.
        Preserves individual word pitch patterns and connects them properly.
        """
        if not group:
            return {'pattern': [], 'accent_positions': [], 'reading': '', 'mora_count': 0}
        
        # Step 1: Combine readings and track word boundaries
        combined_reading = ''
        word_boundaries = []  # Track where each word starts/ends
        current_mora = 0
        
        for token in group:
            reading = token['reading']
            mora_count = len(reading)
            
            # Record word boundaries
            word_boundaries.append({
                'token': token,
                'mora_start': current_mora,
                'mora_end': current_mora + mora_count,
                'reading': reading,
                'drop_pos': token['drop_pos'],
                'pitch_type': token['pitch_type']
            })
            
            combined_reading += reading
            current_mora += mora_count
        
        # Step 2: Generate unified pattern by connecting individual word patterns
        unified_pattern = []
        accent_positions = []
        
        for i, boundary in enumerate(word_boundaries):
            token = boundary['token']
            reading = boundary['reading']
            drop_pos = boundary['drop_pos']
            
            # Get individual word pattern
            word_pattern = get_pitch_pattern(len(reading), drop_pos)
            
            # Get accent positions for this word
            word_accent_positions = get_accent_position(len(reading), drop_pos)
            
            # Connect to previous word's pattern
            if i == 0:
                # First word: use its pattern as starting point
                unified_pattern.extend(word_pattern)
                accent_positions.extend(word_accent_positions)
            else:
                # Subsequent words: apply Japanese pitch accent connection rules
                prev_final_pitch = unified_pattern[-1] if unified_pattern else 'L'
                
                # Adjust first mora of current word based on Japanese rules
                if word_pattern:
                    # JAPANESE PITCH CONNECTION RULES:
                    # 1. Atamadaka words ALWAYS start HIGH (even after low-ending words)
                    # 2. Other words inherit pitch from previous word's final mora
                    # 3. Particles inherit pitch from preceding word
                    
                    if token['pitch_type'] == 1:  # Atamadaka
                        # Atamadaka words always start HIGH
                        adjusted_word_pattern = ['H'] + word_pattern[1:]
                    else:
                        # Other words inherit pitch from previous word
                        adjusted_word_pattern = [prev_final_pitch] + word_pattern[1:]
                    
                    unified_pattern.extend(adjusted_word_pattern)
                    
                    # Adjust accent positions based on the adjusted pattern
                    if token['pitch_type'] == 1:  # Atamadaka
                        # For Atamadaka, if we changed the first mora to HIGH, 
                        # the accent should be on the first mora (which is now HIGH)
                        adjusted_accent_positions = [True] + word_accent_positions[1:]
                    else:
                        # For other words, if we changed the first mora's pitch,
                        # we need to adjust the accent position accordingly
                        if prev_final_pitch != word_pattern[0]:
                            # The first mora's pitch changed, so adjust accent positions
                            # If the first mora was originally accented and is now different pitch,
                            # we need to recalculate
                            if word_accent_positions[0]:  # First mora was accented
                                # Keep accent on first mora (even though pitch changed)
                                adjusted_accent_positions = [True] + word_accent_positions[1:]
                            else:
                                # No accent on first mora, keep as is
                                adjusted_accent_positions = word_accent_positions.copy()
                        else:
                            # No pitch change, keep original accent positions
                            adjusted_accent_positions = word_accent_positions.copy()
                    
                    accent_positions.extend(adjusted_accent_positions)
        
        return {
            'pattern': unified_pattern,
            'accent_positions': accent_positions,
            'reading': combined_reading,
            'mora_count': len(combined_reading),
            'tokens': group,
            'word_boundaries': word_boundaries
        }
    
    def _combine_phrase_results(self, phrase_results: list, original_sentence: str) -> dict:
        """
        Combine all phrase results into a single unified pattern.
        """
        if not phrase_results:
            return {
                'pattern': [],
                'accent_positions': [],
                'reading': '',
                'mora_count': 0,
                'phrases': [],
                'original_sentence': original_sentence
            }
        
        # Combine all phrase results into a single unified pattern
        combined_reading = ''
        combined_pattern = []
        combined_accent_positions = []
        current_mora = 0
        
        for i, phrase_result in enumerate(phrase_results):
            phrase_reading = phrase_result['reading']
            phrase_pattern = phrase_result['pattern']
            phrase_accent_positions = phrase_result['accent_positions']
            
            # Add phrase reading
            combined_reading += phrase_reading
            
            # Add phrase pattern
            combined_pattern.extend(phrase_pattern)
            
            # Add phrase accent positions (adjust mora positions)
            for j, is_accent in enumerate(phrase_accent_positions):
                if is_accent:
                    # Mark the accent mora at the correct position in the combined pattern
                    accent_pos = current_mora + j
                    # Extend accent positions list if needed
                    while len(combined_accent_positions) <= accent_pos:
                        combined_accent_positions.append(False)
                    combined_accent_positions[accent_pos] = True
                else:
                    # Extend accent positions list if needed
                    while len(combined_accent_positions) <= current_mora + j:
                        combined_accent_positions.append(False)
            
            current_mora += len(phrase_pattern)
            
            # Add pause between phrases (except for the last phrase)
            if i < len(phrase_results) - 1:
                # Add a brief pause marker (could be used for visualization)
                pass
        
        return {
            'pattern': combined_pattern,
            'accent_positions': combined_accent_positions,
            'reading': combined_reading,
            'mora_count': len(combined_reading),
            'phrases': phrase_results,
            'original_sentence': original_sentence
        }
    
    def generate_sentence_svg(self, sentence: str) -> str:
        """
        Generate SVG visualization for a sentence.
        """
        result = self.process_sentence(sentence)
        if not result['pattern']:
            return ""
        
        from pitch_svg import generate_pitch_svg
        return generate_pitch_svg(result['pattern'], result['accent_positions'])
    
    def generate_sentence_html(self, sentence: str) -> str:
        """
        Generate HTML visualization for a sentence.
        """
        result = self.process_sentence(sentence)
        if not result['pattern']:
            return ""
        
        from pitch_svg import generate_pitch_html
        return generate_pitch_html(result['pattern'], result['accent_positions'], sentence)

def test_sentence_processor():
    """
    Test the sentence pitch processor with various examples.
    """
    print("🧪 Testing Sentence Pitch Processor")
    print("=" * 50)
    
    processor = SentencePitchProcessor()
    
    # Test sentences
    test_sentences = [
        "大学に行きます",
        "お菓子を食べる", 
        "新しい本を買いました",
        "私は日本語を勉強しています"
    ]
    
    for sentence in test_sentences:
        print(f"\n📝 Sentence: {sentence}")
        result = processor.process_sentence(sentence)
        
        print(f"   Reading: {result['reading']}")
        print(f"   Pattern: {result['pattern']}")
        print(f"   Accent positions: {result['accent_positions']}")
        
        # Create visual representation
        visual = ""
        for pitch, is_accent in zip(result['pattern'], result['accent_positions']):
            if is_accent:
                visual += "○"
            else:
                visual += "●"
        print(f"   Visual: {visual}")
        
        # Generate SVG
        svg = processor.generate_sentence_svg(sentence)
        print(f"   SVG: Generated ({len(svg)} characters)")

if __name__ == "__main__":
    test_sentence_processor() 