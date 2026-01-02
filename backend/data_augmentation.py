"""
Data augmentation for Product Need Model.
Adds broken English, typos, short phrases, and variations to training data.
"""

import pandas as pd
import random
import re
from pathlib import Path
from typing import List, Tuple

# Common typos and variations
TYPO_PATTERNS = {
    'very': ['vey', 'verry', 'vary'],
    'slow': ['slw', 'slwo', 'slo'],
    'computer': ['comuter', 'compter', 'pc', 'laptop'],
    'not': ['not', 'no', 'nt'],
    'start': ['strt', 'start', 'boot', 'turn on'],
    'internet': ['intenet', 'inet', 'wifi', 'wi-fi'],
    'upgrade': ['upgarde', 'upgrade', 'need'],
    'ram': ['ram', 'memory', 'mem'],
    'ssd': ['ssd', 'hard drive', 'hdd'],
    'gpu': ['gpu', 'graphics', 'video card'],
    'psu': ['psu', 'power supply', 'ps'],
    'display': ['display', 'screen', 'monitor'],
    'overheat': ['overheat', 'hot', 'heating'],
}

# Short phrase expansions
SHORT_PHRASE_EXPANSIONS = {
    'pc slow': ['my pc is very slow', 'computer running slow', 'pc performance slow'],
    'ps not start': ['power supply not starting', 'pc wont turn on', 'computer not booting'],
    'no internet': ['no internet connection', 'wifi not working', 'cant connect to internet'],
    'pc hot': ['computer overheating', 'pc getting very hot', 'system temperature high'],
    'no display': ['no display on monitor', 'screen black', 'monitor not showing'],
}

def add_typos(text: str, probability: float = 0.3) -> str:
    """Add typos to text based on common patterns."""
    words = text.split()
    result = []
    
    for word in words:
        word_lower = word.lower()
        if random.random() < probability and word_lower in TYPO_PATTERNS:
            # Replace with typo variation
            typo = random.choice(TYPO_PATTERNS[word_lower])
            result.append(typo)
        else:
            result.append(word)
    
    return ' '.join(result)


def shorten_text(text: str) -> str:
    """Create shortened version of text."""
    # Remove articles, prepositions
    words = text.split()
    short_words = [w for w in words if w.lower() not in ['the', 'a', 'an', 'is', 'are', 'and', 'or', 'but']]
    return ' '.join(short_words[:8])  # Limit to 8 words


def expand_short_phrase(text: str) -> List[str]:
    """Expand short phrases to longer variations."""
    text_lower = text.lower().strip()
    
    for short, expansions in SHORT_PHRASE_EXPANSIONS.items():
        if short in text_lower:
            return expansions
    
    return []


def create_variations(text: str, component: str, num_variations: int = 3) -> List[Tuple[str, str]]:
    """
    Create variations of a text-component pair.
    Returns list of (text, component) tuples.
    """
    variations = []
    
    # Original
    variations.append((text, component))
    
    # Add typos (more aggressive for broken English)
    for _ in range(num_variations * 2):  # More typo variations
        typo_text = add_typos(text, probability=0.3)
        if typo_text != text:
            variations.append((typo_text, component))
    
    # Shortened version (for long texts)
    if len(text.split()) > 5:
        short_text = shorten_text(text)
        if short_text and short_text != text:
            variations.append((short_text, component))
            # Also add typo version of shortened text
            typo_short = add_typos(short_text, probability=0.3)
            if typo_short != short_text:
                variations.append((typo_short, component))
    
    # Very short version (2-3 words) for short phrases
    if len(text.split()) > 3:
        words = text.split()
        very_short = ' '.join(words[:3])  # First 3 words
        if very_short != text:
            variations.append((very_short, component))
    
    # Expanded short phrases
    expansions = expand_short_phrase(text)
    for exp in expansions[:2]:
        if exp and exp != text:
            variations.append((exp, component))
    
    # Add common broken English patterns
    text_lower = text.lower()
    # Remove articles for broken English
    broken_variants = [
        text_lower.replace(' the ', ' ').replace(' a ', ' ').replace(' an ', ' '),
        text_lower.replace(' is ', ' ').replace(' are ', ' '),
    ]
    for variant in broken_variants:
        if variant != text_lower and len(variant.strip()) > 3:
            variations.append((variant.strip(), component))
    
    # Remove duplicates (but be less aggressive)
    seen = set()
    unique_variations = []
    for t, c in variations:
        # Normalize for comparison but keep original
        key = (t.lower().strip()[:50], c)  # Use first 50 chars for dedup
        if key not in seen:
            seen.add(key)
            unique_variations.append((t, c))
    
    return unique_variations


def augment_dataset(input_csv: Path, output_csv: Path, augmentation_factor: int = 2):
    """
    Augment training dataset with variations.
    
    Args:
        input_csv: Path to original training data
        output_csv: Path to save augmented data
        augmentation_factor: How many variations per original sample
    """
    print("=" * 80)
    print("DATA AUGMENTATION FOR PRODUCT NEED MODEL")
    print("=" * 80)
    
    # Load original data
    df = pd.read_csv(input_csv)
    df = df.dropna(subset=['user_text', 'component_label'])
    
    print(f"[INFO] Original dataset: {len(df)} samples")
    
    # Create augmented data
    augmented_rows = []
    
    # Sample subset for augmentation to avoid too much data
    # Augment all samples but limit variations per sample
    sample_size = min(len(df), 5000)  # Limit to 5000 samples for augmentation
    df_sample = df.sample(n=sample_size, random_state=42) if len(df) > sample_size else df
    
    print(f"[INFO] Augmenting {len(df_sample)} samples...")
    
    for idx, row in df_sample.iterrows():
        text = str(row['user_text']).strip()
        component = str(row['component_label']).strip()
        
        # Create variations
        variations = create_variations(text, component, num_variations=augmentation_factor)
        
        for var_text, var_component in variations:
            augmented_rows.append({
                'user_text': var_text,
                'component_label': var_component,
                'component_definition': row.get('component_definition', ''),
                'why_useful': row.get('why_useful', ''),
                'extra_explanation': row.get('extra_explanation', '')
            })
    
    # Combine original + augmented
    print(f"[INFO] Created {len(augmented_rows)} augmented samples")
    
    # Add original data
    for _, row in df.iterrows():
        augmented_rows.append({
            'user_text': str(row['user_text']).strip(),
            'component_label': str(row['component_label']).strip(),
            'component_definition': row.get('component_definition', ''),
            'why_useful': row.get('why_useful', ''),
            'extra_explanation': row.get('extra_explanation', '')
        })
    
    # Create DataFrame and deduplicate (less aggressive)
    df_combined = pd.DataFrame(augmented_rows)
    # Only remove exact duplicates
    df_augmented = df_combined.drop_duplicates(subset=['user_text', 'component_label'], keep='first')
    
    print(f"[INFO] Augmented dataset: {len(df_augmented)} samples")
    print(f"[INFO] Increase: {len(df_augmented) - len(df)} samples ({len(df_augmented)/len(df):.1f}x)")
    
    # Save
    df_augmented.to_csv(output_csv, index=False)
    print(f"[INFO] Saved to: {output_csv}")
    
    return df_augmented


if __name__ == "__main__":
    HERE = Path(__file__).parent.resolve()
    DATA_DIR = (HERE.parent / "data").resolve()
    
    input_csv = DATA_DIR / "hardware_component_dataset_merged.csv"
    output_csv = DATA_DIR / "hardware_component_dataset_augmented.csv"
    
    if not input_csv.exists():
        print(f"[ERROR] Input file not found: {input_csv}")
    else:
        augment_dataset(input_csv, output_csv, augmentation_factor=2)

