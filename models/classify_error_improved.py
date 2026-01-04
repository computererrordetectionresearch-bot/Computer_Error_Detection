# FILE: models/classify_error_improved.py
import pandas as pd
import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from functools import lru_cache

# Cache for loaded data
_error_categories_cache = None

@lru_cache(maxsize=128)
def load_error_categories():
    """Load error categories from CSV with caching"""
    global _error_categories_cache
    if _error_categories_cache is not None:
        return _error_categories_cache
    
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'error_category.csv')
    df = pd.read_csv(csv_path)
    _error_categories_cache = df
    return df

def extract_keywords_improved(text):
    """Improved keyword extraction with better stopword handling"""
    if not text:
        return []
    
    # Extended stopwords list
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
        'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
        'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'now'
    }
    
    # Extract words (3+ characters, alphanumeric)
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    
    # Filter stopwords and return unique keywords
    keywords = [w for w in words if w not in stopwords]
    return list(set(keywords))  # Remove duplicates

@lru_cache(maxsize=256)
def calculate_similarity_improved(text1, text2):
    """Improved TF-IDF similarity with n-grams"""
    if not text1 or not text2:
        return 0.0
    
    # Use n-grams (1-2 words) for better matching
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),  # Unigrams and bigrams
        min_df=1,
        max_df=0.95,
        lowercase=True,
        strip_accents='unicode'
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except Exception as e:
        return 0.0

def calculate_jaccard_similarity(set1, set2):
    """Calculate Jaccard similarity between two sets"""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0

def classify_error_improved(error_text):
    """Improved error classification with better scoring"""
    if not error_text or len(error_text.strip()) == 0:
        return None
    
    df = load_error_categories()
    normalized_input = error_text.lower().strip()
    input_keywords = set(extract_keywords_improved(error_text))
    
    best_match = None
    best_score = 0.0
    scores = []
    
    for _, row in df.iterrows():
        category_text = row['error_text'].lower()
        score = 0.0
        
        # 1. Exact/substring match (40% weight) - highest priority
        if normalized_input == category_text:
            score += 0.4
        elif normalized_input in category_text or category_text in normalized_input:
            score += 0.3
        elif any(word in category_text for word in normalized_input.split()):
            score += 0.2
        
        # 2. TF-IDF similarity with n-grams (35% weight)
        similarity = calculate_similarity_improved(error_text, row['error_text'])
        score += similarity * 0.35
        
        # 3. Keyword Jaccard similarity (15% weight)
        category_keywords = set(extract_keywords_improved(row['error_text']))
        if input_keywords or category_keywords:
            jaccard = calculate_jaccard_similarity(input_keywords, category_keywords)
            score += jaccard * 0.15
        
        # 4. Keyword overlap count (10% weight)
        common_keywords = input_keywords & category_keywords
        if input_keywords:
            keyword_overlap = len(common_keywords) / len(input_keywords)
            score += keyword_overlap * 0.10
        
        scores.append((score, row['category']))
        
        if score > best_score:
            best_score = score
            best_match = row['category']
    
    # If best score is too low, use default
    if best_score < 0.15:
        return 'Application Crash / App Closing'
    
    return best_match

def is_error_request_improved(text):
    """Improved error detection with better keyword matching"""
    if not text:
        return False
    
    # Extended error keywords with variations
    error_keywords = [
        'error', 'errors', 'failed', 'fails', 'failure', 'crash', 'crashes', 'crashed', 'crashing',
        'closing', 'closed', 'close', 'missing', 'miss', 'denied', 'deny', 'denial',
        'permission', 'permissions', 'dll', 'dlls', 'library', 'libraries', 'librarie',
        'network', 'networking', 'license', 'licensing', 'licence', 'activation', 'activate',
        'problem', 'problems', 'issue', 'issues', 'bug', 'bugs', 'broken', 'break',
        'not working', 'wont work', "won't work", 'doesnt work', "doesn't work",
        'exception', 'exceptions', 'fault', 'faults', 'corrupt', 'corrupted', 'corruption',
        'invalid', 'invalidated', 'timeout', 'timeouts', 'unable', 'cannot', "can't",
        'access denied', 'permission denied', 'installation failed', 'setup failed'
    ]
    
    normalized_text = text.lower()
    
    # Check for exact keyword matches
    for keyword in error_keywords:
        if keyword in normalized_text:
            return True
    
    # Check for error patterns
    error_patterns = [
        r'\berror\b', r'\bfailed\b', r'\bcrashed\b', r'\bmissing\b',
        r'\bdenied\b', r'\bnot working\b', r'\bwont work\b'
    ]
    
    for pattern in error_patterns:
        if re.search(pattern, normalized_text):
            return True
    
    return False

# Export improved functions
def classify_error(error_text):
    """Wrapper for improved classification"""
    return classify_error_improved(error_text)

def is_error_request(text):
    """Wrapper for improved error detection"""
    return is_error_request_improved(text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python classify_error_improved.py <error_text>")
        sys.exit(1)
    
    error_text = sys.argv[1]
    result = classify_error(error_text)
    print(result if result else "null")

