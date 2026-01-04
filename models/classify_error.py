# FILE: models/classify_error.py
import pandas as pd
import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def load_error_categories():
    """Load error categories from CSV"""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'error_category.csv')
    df = pd.read_csv(csv_path)
    return df

def extract_keywords(text):
    """Extract keywords from text"""
    if not text:
        return []
    # Simple keyword extraction: remove stopwords and short words
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can'}
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    return [w for w in words if w not in stopwords]

def calculate_similarity(text1, text2):
    """Calculate TF-IDF cosine similarity with n-grams"""
    if not text1 or not text2:
        return 0.0
    
    # Use n-grams for better matching
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),  # Unigrams and bigrams
        min_df=1,
        max_df=0.95,
        lowercase=True
    )
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except:
        return 0.0

def classify_error(error_text):
    """Classify error text into a category - Improved version"""
    if not error_text or len(error_text.strip()) == 0:
        return None
    
    df = load_error_categories()
    normalized_input = error_text.lower().strip()
    input_keywords = set(extract_keywords(error_text))
    
    best_match = None
    best_score = 0.0
    
    for _, row in df.iterrows():
        category_text = row['error_text'].lower()
        score = 0.0
        
        # 1. Exact/substring match (40% weight)
        if normalized_input == category_text:
            score += 0.4
        elif normalized_input in category_text or category_text in normalized_input:
            score += 0.3
        elif any(word in category_text for word in normalized_input.split()):
            score += 0.2
        
        # 2. TF-IDF similarity (35% weight)
        similarity = calculate_similarity(error_text, row['error_text'])
        score += similarity * 0.35
        
        # 3. Keyword Jaccard similarity (15% weight)
        category_keywords = set(extract_keywords(row['error_text']))
        if input_keywords or category_keywords:
            intersection = len(input_keywords & category_keywords)
            union = len(input_keywords | category_keywords)
            jaccard = intersection / union if union > 0 else 0.0
            score += jaccard * 0.15
        
        # 4. Keyword overlap (10% weight)
        if input_keywords:
            common_keywords = input_keywords & category_keywords
            keyword_overlap = len(common_keywords) / len(input_keywords)
            score += keyword_overlap * 0.10
        
        if score > best_score:
            best_score = score
            best_match = row['category']
    
    if best_score < 0.15:
        return 'Application Crash / App Closing'
    
    return best_match

def is_error_request(text):
    """Check if text is an error request"""
    error_keywords = [
        'error', 'failed', 'crash', 'closing', 'missing', 'denied',
        'permission', 'dll', 'library', 'network', 'license', 'activation',
        'problem', 'issue', 'bug', 'broken', 'not working'
    ]
    
    normalized_text = text.lower()
    return any(keyword in normalized_text for keyword in error_keywords)

if __name__ == '__main__':
    # Command line interface
    if len(sys.argv) < 2:
        print("Usage: python classify_error.py <error_text>")
        sys.exit(1)
    
    error_text = sys.argv[1]
    result = classify_error(error_text)
    print(result if result else "null")

