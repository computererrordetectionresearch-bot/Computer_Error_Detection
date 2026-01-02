"""
Retrain hierarchical models with user feedback.
Merges feedback data with original training data and retrains both models.
"""

from pathlib import Path
import pandas as pd
import joblib
import json
import sys
import io
from datetime import datetime
import shutil
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()
FEEDBACK_CSV = DATA_DIR / "product_need_feedback.csv"
MAPPING_PATH = HERE / "component_category_mapping.json"

# Model paths with versioning
CATEGORY_MODEL_PATH = HERE / "product_need_category_model.pkl"
COMPONENT_MODEL_PATH = HERE / "product_need_component_model.pkl"

# Backup old models
def backup_models():
    """Backup existing models before retraining."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if CATEGORY_MODEL_PATH.exists():
        backup_path = HERE / f"product_need_category_model_backup_{timestamp}.pkl"
        shutil.copy2(CATEGORY_MODEL_PATH, backup_path)
        print(f"✅ Backed up category model to: {backup_path}")
    
    if COMPONENT_MODEL_PATH.exists():
        backup_path = HERE / f"product_need_component_model_backup_{timestamp}.pkl"
        shutil.copy2(COMPONENT_MODEL_PATH, backup_path)
        print(f"✅ Backed up component model to: {backup_path}")


def merge_feedback_with_training():
    """
    Merge feedback data with original training data.
    Uses user_correct_label if provided, otherwise uses predicted_label.
    """
    # Load original training data
    HARDWARE_CSV = DATA_DIR / "hardware_component_dataset_merged.csv"
    df_original = pd.read_csv(HARDWARE_CSV)
    df_original = df_original.dropna(subset=['user_text', 'component_label'])
    df_original['text'] = df_original['user_text'].astype(str).str.lower().str.strip()
    
    print(f"📊 Original training data: {len(df_original)} samples")
    
    # Load feedback data
    if not FEEDBACK_CSV.exists():
        print("ℹ️ No feedback data found. Using original training data only.")
        return df_original
    
    df_feedback = pd.read_csv(FEEDBACK_CSV)
    
    if df_feedback.empty:
        print("ℹ️ Feedback file is empty. Using original training data only.")
        return df_original
    
    print(f"📊 Feedback data: {len(df_feedback)} entries")
    
    # Filter feedback with corrections
    df_feedback = df_feedback[df_feedback['user_correct_label'].notna()]
    df_feedback = df_feedback[df_feedback['user_correct_label'] != '']
    
    print(f"📊 Feedback with corrections: {len(df_feedback)} entries")
    
    if df_feedback.empty:
        print("ℹ️ No feedback with corrections. Using original training data only.")
        return df_original
    
    # Create training rows from feedback
    feedback_rows = []
    for _, row in df_feedback.iterrows():
        feedback_rows.append({
            'user_text': row['user_text'],
            'component_label': row['user_correct_label'],
            'component_definition': '',  # Will be filled from mapping if needed
            'why_useful': '',
            'extra_explanation': ''
        })
    
    df_feedback_training = pd.DataFrame(feedback_rows)
    df_feedback_training['text'] = df_feedback_training['user_text'].astype(str).str.lower().str.strip()
    
    # Merge with original data
    df_merged = pd.concat([df_original, df_feedback_training], ignore_index=True)
    df_merged = df_merged.drop_duplicates(subset=['text', 'component_label'])
    
    print(f"📊 Merged training data: {len(df_merged)} samples")
    print(f"   - Original: {len(df_original)}")
    print(f"   - Feedback: {len(df_feedback_training)}")
    print(f"   - After deduplication: {len(df_merged)}")
    
    return df_merged


def retrain_models():
    """Retrain both category and component models with merged data."""
    print("=" * 80)
    print("RETRAINING MODELS WITH FEEDBACK")
    print("=" * 80)
    
    # Backup existing models
    backup_models()
    
    # Merge feedback with training data
    df = merge_feedback_with_training()
    
    # Load mapping
    with open(MAPPING_PATH, 'r', encoding='utf-8') as f:
        category_mapping = json.load(f)
    
    component_to_category = {}
    for category, components in category_mapping.items():
        for component in components:
            component_to_category[component] = category
    
    # Map components to categories
    df['category'] = df['component_label'].map(component_to_category)
    df = df.dropna(subset=['category'])
    
    print(f"\n📊 Final training data: {len(df)} samples")
    print(f"📊 Categories: {df['category'].nunique()}")
    print(f"📊 Components: {df['component_label'].nunique()}")
    
    # Train category model
    print("\n" + "=" * 80)
    print("RETRAINING CATEGORY MODEL")
    print("=" * 80)
    
    X_category = df['text'].values
    y_category = df['category'].values
    
    try:
        X_cat_train, X_cat_test, y_cat_train, y_cat_test = train_test_split(
            X_category, y_category, test_size=0.2, random_state=42, stratify=y_category
        )
    except:
        X_cat_train, X_cat_test, y_cat_train, y_cat_test = train_test_split(
            X_category, y_category, test_size=0.2, random_state=42
        )
    
    # Use same feature union as training script
    word_tfidf = TfidfVectorizer(
        ngram_range=(1, 2), min_df=2, max_df=0.95, sublinear_tf=True,
        stop_words='english', analyzer='word'
    )
    char_tfidf = TfidfVectorizer(
        ngram_range=(3, 5), min_df=2, max_df=0.95, sublinear_tf=True, analyzer='char'
    )
    feature_union = FeatureUnion([('word_tfidf', word_tfidf), ('char_tfidf', char_tfidf)])
    
    category_model = Pipeline([
        ('features', feature_union),
        ('clf', SGDClassifier(random_state=42, max_iter=1000, loss='log_loss'))
    ])
    
    category_model.fit(X_cat_train, y_cat_train)
    cat_accuracy = accuracy_score(y_cat_test, category_model.predict(X_cat_test))
    
    print(f"✅ Category Model Accuracy: {cat_accuracy:.4f}")
    joblib.dump(category_model, CATEGORY_MODEL_PATH)
    print(f"💾 Saved to: {CATEGORY_MODEL_PATH}")
    
    # Train component model
    print("\n" + "=" * 80)
    print("RETRAINING COMPONENT MODEL")
    print("=" * 80)
    
    X_component = df['text'].values
    y_component = df['component_label'].values
    
    # Filter valid classes
    class_counts = pd.Series(y_component).value_counts()
    valid_classes = class_counts[class_counts >= 2].index
    df_filtered = df[df['component_label'].isin(valid_classes)]
    
    if len(df_filtered) < len(df) * 0.8:
        X_component = df_filtered['text'].values
        y_component = df_filtered['component_label'].values
    
    try:
        X_comp_train, X_comp_test, y_comp_train, y_comp_test = train_test_split(
            X_component, y_component, test_size=0.2, random_state=42, stratify=y_component
        )
    except:
        X_comp_train, X_comp_test, y_comp_train, y_comp_test = train_test_split(
            X_component, y_component, test_size=0.2, random_state=42
        )
    
    feature_union_comp = FeatureUnion([
        ('word_tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95, sublinear_tf=True, stop_words='english', analyzer='word')),
        ('char_tfidf', TfidfVectorizer(ngram_range=(3, 5), min_df=2, max_df=0.95, sublinear_tf=True, analyzer='char'))
    ])
    
    component_model = Pipeline([
        ('features', feature_union_comp),
        ('clf', SGDClassifier(random_state=42, max_iter=1000, loss='log_loss'))
    ])
    
    component_model.fit(X_comp_train, y_comp_train)
    comp_accuracy = accuracy_score(y_comp_test, component_model.predict(X_comp_test))
    
    print(f"✅ Component Model Accuracy: {comp_accuracy:.4f}")
    joblib.dump(component_model, COMPONENT_MODEL_PATH)
    print(f"💾 Saved to: {COMPONENT_MODEL_PATH}")
    
    print("\n" + "=" * 80)
    print("RETRAINING COMPLETE")
    print("=" * 80)
    print(f"✅ Category Model: {cat_accuracy:.4f}")
    print(f"✅ Component Model: {comp_accuracy:.4f}")


if __name__ == "__main__":
    retrain_models()

