# FILE: models/match_error_fix_improved.py
import pandas as pd
import sys
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache

# Cache for loaded data
_error_fixes_cache = None
_feedback_stats_cache = None

@lru_cache(maxsize=1)
def load_error_fixes():
    """Load error fixes from CSV with caching"""
    global _error_fixes_cache
    if _error_fixes_cache is not None:
        return _error_fixes_cache
    
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'error_fix_dataset.csv')
    df = pd.read_csv(csv_path)
    df['id'] = df['id'].astype(int)
    _error_fixes_cache = df
    return df

@lru_cache(maxsize=1)
def load_feedback_stats():
    """Load feedback statistics with caching"""
    global _feedback_stats_cache
    if _feedback_stats_cache is not None:
        return _feedback_stats_cache
    
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'feedback.csv')
    
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            _feedback_stats_cache = {}
            return {}
        
        stats = {}
        for fix_id in df['fix_id'].unique():
            fix_feedback = df[df['fix_id'] == fix_id]
            total = len(fix_feedback)
            success = len(fix_feedback[fix_feedback['success'].isin(['true', '1', True, 1])])
            stats[int(fix_id)] = {
                'success_count': int(success),
                'total_count': int(total),
                'success_rate': success / total if total > 0 else 0.0
            }
        _feedback_stats_cache = stats
        return stats
    except:
        _feedback_stats_cache = {}
        return {}

@lru_cache(maxsize=512)
def calculate_similarity_improved(text1, text2):
    """Improved TF-IDF similarity with better vectorization"""
    if not text1 or not text2:
        return 0.0
    
    # Use n-grams and better preprocessing
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),  # Unigrams and bigrams
        min_df=1,
        max_df=0.95,
        lowercase=True,
        strip_accents='unicode',
        analyzer='word'
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except:
        return 0.0

def match_error_fix_improved(error_text, software, os_name, category):
    """Improved error-fix matching with better scoring"""
    df = load_error_fixes()
    feedback_stats = load_feedback_stats()
    
    normalized_software = software.strip().lower()
    normalized_os = os_name.strip().lower()
    normalized_category = category.strip().lower()
    normalized_error = error_text.lower().strip()
    
    # Filter by software and OS
    candidates = df[
        (df['software'].str.lower() == normalized_software) &
        (df['os'].str.lower() == normalized_os)
    ].copy()
    
    if candidates.empty:
        return None
    
    # Score each candidate with improved algorithm
    scored_candidates = []
    for _, fix in candidates.iterrows():
        score = 0.0
        fix_error_msg = fix['error_message'].lower()
        
        # 1. Error message similarity with n-grams (50% weight)
        error_similarity = calculate_similarity_improved(normalized_error, fix_error_msg)
        score += error_similarity * 0.50
        
        # 2. Exact error message match (15% weight) - high priority
        if normalized_error == fix_error_msg:
            score += 0.15
        elif normalized_error in fix_error_msg or fix_error_msg in normalized_error:
            score += 0.10
        
        # 3. Category match in error message (15% weight)
        if normalized_category in fix_error_msg or fix_error_msg in normalized_category:
            score += 0.15
        else:
            # Partial category match
            category_words = set(normalized_category.split())
            error_words = set(fix_error_msg.split())
            if category_words & error_words:
                score += 0.05
        
        # 4. Feedback success rate (15% weight) - learned from user feedback
        stats = feedback_stats.get(fix['id'])
        if stats and stats['total_count'] > 0:
            # Use success rate, but require minimum 3 feedbacks for reliability
            if stats['total_count'] >= 3:
                success_rate = stats['success_count'] / stats['total_count']
                score += success_rate * 0.15
            else:
                # For new fixes, give small boost if any positive feedback
                if stats['success_count'] > 0:
                    score += 0.05
        
        # 5. Probable cause similarity (5% weight)
        probable_cause = str(fix.get('probable_cause', '')).lower()
        if probable_cause:
            cause_similarity = calculate_similarity_improved(normalized_error, probable_cause)
            score += cause_similarity * 0.05
        
        # Only include candidates with meaningful scores
        if score > 0.15:
            scored_candidates.append({
                'fix': fix.to_dict(),
                'score': score
            })
    
    if not scored_candidates:
        return None
    
    # Sort by score and return best match
    scored_candidates.sort(key=lambda x: x['score'], reverse=True)
    return scored_candidates[0]

# Export improved function
def match_error_fix(error_text, software, os_name, category):
    """Wrapper for improved matching"""
    return match_error_fix_improved(error_text, software, os_name, category)

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python match_error_fix_improved.py <error_text> <software> <os> <category>")
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

