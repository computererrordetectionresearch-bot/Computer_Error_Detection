"""
Train product category classification model.
Classifies product category (GPU, SSD, RAM, Wi-Fi Adapter, PSU) from user symptoms.
"""

from pathlib import Path
import pandas as pd
import sys
import io
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()
MODEL_PATH = HERE / "nlp_error_model_product.pkl"

def load_training_data():
    """Load all available product category training data."""
    dfs = []
    
    # Load main product texts
    PRODUCT_TEXTS_CSV = DATA_DIR / "product_texts.csv"
    if PRODUCT_TEXTS_CSV.exists():
        df = pd.read_csv(PRODUCT_TEXTS_CSV)
        if 'text' in df.columns and 'product_category' in df.columns:
            df = df.rename(columns={'text': 'user_text'})
            dfs.append(df)
            print(f"[INFO] Loaded {len(df)} samples from product_texts.csv")
    
    if not dfs:
        print("[ERROR] No training data found!")
        return None
    
    # Combine all data
    df_all = pd.concat(dfs, ignore_index=True)
    df_all = df_all.dropna(subset=['user_text', 'product_category'])
    df_all['user_text'] = df_all['user_text'].astype(str).str.strip()
    df_all = df_all[df_all['user_text'].str.len() > 0]
    
    # Remove duplicates
    df_all = df_all.drop_duplicates(subset=['user_text', 'product_category'])
    
    print(f"\n[INFO] Total training samples: {len(df_all)}")
    print(f"[INFO] Product categories: {df_all['product_category'].nunique()}")
    print(f"\nCategory distribution:")
    print(df_all['product_category'].value_counts())
    
    return df_all

def train_model():
    """Train the product category classification model."""
    print("\n" + "=" * 80)
    print("TRAINING PRODUCT CATEGORY CLASSIFICATION MODEL")
    print("=" * 80)
    
    # Load data
    df = load_training_data()
    if df is None:
        return False, 0.0
    
    # Prepare data
    X = df['user_text'].values
    y = df['product_category'].values
    
    # Filter classes with at least 2 samples
    from collections import Counter
    class_counts = Counter(y)
    valid_classes = {cls for cls, count in class_counts.items() if count >= 2}
    valid_mask = pd.Series(y).isin(valid_classes)
    X = X[valid_mask]
    y = y[valid_mask]
    
    print(f"\n[INFO] After filtering: {len(X)} samples, {len(set(y))} classes")
    
    # Split data
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    except ValueError:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    
    print(f"\n[INFO] Training samples: {len(X_train)}")
    print(f"[INFO] Test samples: {len(X_test)}")
    
    # Create pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=10000,
            min_df=1,
            max_df=0.95
        )),
        ('classifier', SGDClassifier(
            loss='log_loss',
            alpha=0.0001,
            max_iter=2000,
            random_state=42,
            n_jobs=-1
        ))
    ])
    
    # Train model
    print("\n[INFO] Training model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n[INFO] Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("\n[INFO] Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Save model
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\n[SUCCESS] Model saved to: {MODEL_PATH}")
    
    return True, accuracy

if __name__ == "__main__":
    print("=" * 80)
    print("PRODUCT CATEGORY MODEL TRAINING")
    print("=" * 80)
    
    success, accuracy = train_model()
    
    if success:
        print(f"\n{'='*80}")
        print(f"TRAINING COMPLETE")
        print(f"{'='*80}")
        print(f"Accuracy: {accuracy:.2%}")
        print(f"Model saved to: {MODEL_PATH}")
        print(f"{'='*80}")
    else:
        print("\n[ERROR] Training failed!")
        sys.exit(1)

