# FILE: models/match_error_fix.py
import pandas as pd
import sys
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_error_fixes():
    """Load error fixes from CSV"""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'error_fix_dataset.csv')
    df = pd.read_csv(csv_path)
    df['id'] = df['id'].astype(int)
    return df

def load_feedback_stats():
    """Load feedback statistics from CSV"""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'feedback.csv')
    
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            return {}
        
        # Calculate success rates per fix_id
        stats = {}
        for fix_id in df['fix_id'].unique():
            fix_feedback = df[df['fix_id'] == fix_id]
            total = len(fix_feedback)
            success = len(fix_feedback[fix_feedback['success'].isin(['true', '1', True, 1])])
            stats[int(fix_id)] = {
                'success_count': int(success),
                'total_count': int(total)
            }
        return stats
    except:
        return {}

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

def match_error_fix(error_text, software, os_name, category):
    """Match error to best fix - Improved version"""
    df = load_error_fixes()
    feedback_stats = load_feedback_stats()
    
    normalized_software = software.strip().lower()
    normalized_os = os_name.strip().lower()
    normalized_category = category.strip().lower()
    normalized_error = error_text.lower().strip()
    
    # First try: Filter by software and OS (exact match)
    candidates = df[
        (df['software'].str.lower() == normalized_software) &
        (df['os'].str.lower() == normalized_os)
    ].copy()
    
    # Fallback: If no exact match, try same software on any OS
    if candidates.empty:
        candidates = df[
            (df['software'].str.lower() == normalized_software)
        ].copy()
    
    # Last resort: Try same OS with any software (for generic errors)
    if candidates.empty:
        candidates = df[
            (df['os'].str.lower() == normalized_os)
        ].copy()
    
    if candidates.empty:
        return None
    
    # Score each candidate with improved algorithm
    scored_candidates = []
    
    for _, fix in candidates.iterrows():
        score = 0.0
        fix_error_msg = fix['error_message'].lower()
        fix_software = fix['software'].lower()
        fix_os = fix['os'].lower()
        
        # Software and OS match bonus
        software_match = 1.0 if fix_software == normalized_software else 0.5
        os_match = 1.0 if fix_os == normalized_os else 0.5
        
        # 1. Error message similarity with n-grams (45% weight)
        error_similarity = calculate_similarity(normalized_error, fix_error_msg)
        score += error_similarity * 0.45 * software_match * os_match
        
        # 2. Exact error message match (20% weight) - highest priority
        if normalized_error == fix_error_msg:
            score += 0.20 * software_match * os_match
        elif normalized_error in fix_error_msg or fix_error_msg in normalized_error:
            score += 0.15 * software_match * os_match
        # Check for word-level matches
        elif any(word in fix_error_msg for word in normalized_error.split() if len(word) > 3):
            score += 0.10 * software_match * os_match
        
        # 3. Category match (15% weight)
        if normalized_category in fix_error_msg or fix_error_msg in normalized_category:
            score += 0.15 * software_match * os_match
        else:
            # Partial category match
            category_words = set(normalized_category.split())
            error_words = set(fix_error_msg.split())
            if category_words & error_words:
                score += 0.05 * software_match * os_match
        
        # 4. Feedback success rate (15% weight) - requires minimum feedbacks
        stats = feedback_stats.get(fix['id'])
        if stats and stats['total_count'] > 0:
            if stats['total_count'] >= 3:  # Require at least 3 feedbacks for reliability
                success_rate = stats['success_count'] / stats['total_count']
                score += success_rate * 0.15
            elif stats['success_count'] > 0:
                score += 0.05  # Small boost for new fixes with positive feedback
        
        # 5. Probable cause similarity (5% weight)
        probable_cause = str(fix.get('probable_cause', '')).lower()
        if probable_cause:
            cause_similarity = calculate_similarity(normalized_error, probable_cause)
            score += cause_similarity * 0.05 * software_match * os_match
        
        # Lower threshold to catch more matches
        if score > 0.12:
            scored_candidates.append({
                'fix': fix.to_dict(),
                'score': score
            })
    
    if not scored_candidates:
        return None
    
    # Return best match
    best = max(scored_candidates, key=lambda x: x['score'])
    return best

if __name__ == '__main__':
    # Command line interface
    if len(sys.argv) < 5:
        print("Usage: python match_error_fix.py <error_text> <software> <os> <category>")
        sys.exit(1)
    
    error_text = sys.argv[1]
    software = sys.argv[2]
    os_name = sys.argv[3]
    category = sys.argv[4]
    
    result = match_error_fix(error_text, software, os_name, category)
    
    if result:
        output = {
            'fix': result['fix'],
            'score': result['score']
        }
        print(json.dumps(output))
    else:
        print("null")

