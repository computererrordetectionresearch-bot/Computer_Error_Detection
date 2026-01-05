"""
Simple spell checker for PC/hardware-related terms.
Uses edit distance (Levenshtein) to suggest corrections for common typos.
"""

# Dictionary of common PC/hardware terms
PC_TERMS = {
    # Common words
    "pc", "computer", "laptop", "desktop", "system",
    "slow", "slowly", "speed", "fast", "quick",
    "much", "many", "too", "very", "really", "really",
    "i", "is", "are", "my", "the", "a", "an", "and", "or",
    "not", "no", "yes", "need", "want", "have", "has",
    "when", "while", "during", "after", "before",
    "to", "up", "down", "in", "on", "at", "for", "with", "from",
    
    # Performance terms
    "performance", "lag", "lagging", "freeze", "freezing", "frozen",
    "stutter", "stuttering", "hang", "hanging", "crash", "crashing",
    "overheat", "overheating", "hot", "heat", "temperature",
    "fps", "frame", "frames", "graphics", "gpu", "cpu",
    
    # Storage terms
    "storage", "space", "full", "empty", "disk", "drive", "hard",
    "ssd", "hdd", "memory", "ram", "upgrade", "upgrading",
    
    # Network terms
    "wifi", "wi-fi", "wireless", "internet", "network", "connection",
    "connect", "disconnect", "disconnecting", "signal", "speed",
    
    # Display terms
    "screen", "display", "monitor", "black", "blue", "white", "color",
    "bright", "brightness", "resolution", "pixel", "pixels",
    
    # Audio terms
    "sound", "audio", "speaker", "speakers", "microphone", "mic",
    "volume", "loud", "quiet", "noise", "static",
    
    # Gaming terms
    "game", "games", "gaming", "gamer", "play", "playing", "run", "running",
    
    # Problem terms
    "problem", "issue", "error", "wrong", "broken", "damaged", "not working",
    "work", "working", "fix", "repair", "repairing", "broken",
    
    # Hardware components
    "keyboard", "mouse", "mousepad", "webcam", "camera", "microphone",
    "processor", "motherboard", "power", "supply", "psu", "cooling", "fan", "fans",
    
    # Action terms
    "start", "starting", "boot", "booting", "shutdown", "shut", "down",
    "turn", "turning", "on", "off", "open", "opening", "close", "closing",
    "load", "loading", "install", "installing", "update", "updating",
}

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein (edit) distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def suggest_correction(word: str, max_distance: int = 2) -> str:
    """
    Suggest correction for a word if it's close to a known term.
    
    Args:
        word: The word to check
        max_distance: Maximum edit distance to consider (default: 2)
    
    Returns:
        Corrected word if found, otherwise original word
    """
    word_lower = word.lower().strip()
    
    # If already correct, return as-is
    if word_lower in PC_TERMS:
        return word
    
    # Don't correct very short words (1-2 letters) unless they're clearly wrong
    # This prevents "i" from being corrected to "is", "a" to "an", etc.
    if len(word_lower) <= 2:
        # Only correct if it's a known typo pattern
        common_typos = {
            "ii": "i", "im": "i'm", "id": "i'd", "ive": "i've",
            "ur": "your", "u": "you", "r": "are", "y": "why"
        }
        if word_lower in common_typos:
            return common_typos[word_lower]
        # Otherwise, don't correct short words
        return word
    
    # Find closest match
    best_match = None
    best_distance = max_distance + 1
    
    for term in PC_TERMS:
        # Skip very short terms when the word is also short (to avoid "i" -> "is")
        if len(word_lower) <= 2 and len(term) <= 2:
            continue
        distance = levenshtein_distance(word_lower, term)
        if distance < best_distance:
            best_distance = distance
            best_match = term
            if distance == 0:  # Exact match (shouldn't happen, but just in case)
                break
    
    # Return correction if found, otherwise return original
    # Be more conservative: only correct if distance is 1 (single character difference)
    # and the word is at least 3 characters long
    if best_match and best_distance <= max_distance:
        # For short words, only correct if it's a very close match (distance 1)
        if len(word_lower) <= 3 and best_distance > 1:
            return word
        # Preserve original capitalization if first letter was uppercase
        if word and word[0].isupper():
            return best_match.capitalize()
        return best_match
    
    return word


def check_and_correct(text: str) -> tuple[str, list[str]]:
    """
    Check text for typos and suggest corrections.
    
    Args:
        text: Input text to check
    
    Returns:
        Tuple of (corrected_text, list_of_corrections)
        corrections format: [(original_word, suggested_word), ...]
    """
    import re
    
    words = re.findall(r'\b\w+\b', text)
    corrections = []
    corrected_words = []
    
    for word in words:
        corrected = suggest_correction(word)
        if corrected.lower() != word.lower():
            corrections.append((word, corrected))
        corrected_words.append(corrected)
    
    # Reconstruct text with corrections
    corrected_text = text
    for original, corrected in corrections:
        # Replace word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(original) + r'\b'
        corrected_text = re.sub(pattern, corrected, corrected_text, count=1)
    
    return corrected_text, corrections


def get_correction_suggestion(original_text: str, corrected_text: str, corrections: list) -> str:
    """
    Generate a user-friendly correction suggestion message.
    
    Args:
        original_text: Original input text
        corrected_text: Corrected text
        corrections: List of (original, corrected) tuples
    
    Returns:
        Suggestion message string - just the corrected sentence
    """
    if not corrections:
        return ""
    
    # Return just the corrected text in a simple format
    return corrected_text

