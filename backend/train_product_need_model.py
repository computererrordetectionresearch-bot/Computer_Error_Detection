"""
Train product need (hardware component) classification model.
Recommends specific hardware components based on user problem descriptions.
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
MODEL_PATH = HERE / "product_need_model.pkl"

def load_training_data():
    """Load all available product need training data."""
    dfs = []
    
    # Load merged hardware component dataset
    HARDWARE_CSV = DATA_DIR / "hardware_component_dataset_merged.csv"
    if HARDWARE_CSV.exists():
        df = pd.read_csv(HARDWARE_CSV)
        if 'user_text' in df.columns and 'component_label' in df.columns:
            dfs.append(df[['user_text', 'component_label']])
            print(f"[INFO] Loaded {len(df)} samples from hardware_component_dataset_merged.csv")
    
    # Try other hardware datasets
    for dataset_file in ["hardware_component_dataset_10000.csv", 
                        "hardware_component_dataset_improved.csv",
                        "hardware_component_dataset_augmented.csv"]:
        dataset_path = DATA_DIR / dataset_file
        if dataset_path.exists():
            df = pd.read_csv(dataset_path)
            if 'user_text' in df.columns and 'component_label' in df.columns:
                dfs.append(df[['user_text', 'component_label']])
                print(f"[INFO] Loaded {len(df)} samples from {dataset_file}")
    
    if not dfs:
        print("[ERROR] No training data found!")
        return None
    
    # Combine all data
    df_all = pd.concat(dfs, ignore_index=True)
    df_all = df_all.dropna(subset=['user_text', 'component_label'])
    df_all['user_text'] = df_all['user_text'].astype(str).str.strip()
    df_all = df_all[df_all['user_text'].str.len() > 0]
    
    # Remove duplicates
    df_all = df_all.drop_duplicates(subset=['user_text', 'component_label'])
    
    print(f"\n[INFO] Total training samples: {len(df_all)}")
    print(f"[INFO] Component types: {df_all['component_label'].nunique()}")
    print(f"\nTop 20 component distribution:")
    print(df_all['component_label'].value_counts().head(20))
    
    return df_all

def train_model():
    """Train the product need classification model."""
    print("\n" + "=" * 80)
    print("TRAINING PRODUCT NEED (COMPONENT) CLASSIFICATION MODEL")
    print("=" * 80)
    
    # Load data
    df = load_training_data()
    if df is None:
        return False, 0.0
    
    # Prepare data
    X = df['user_text'].values
    y = df['component_label'].values
    
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
            max_features=20000,
            min_df=2,
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
    print("\n[INFO] Classification Report (top 20 classes):")
    # Show report for most common classes
    top_classes = pd.Series(y_test).value_counts().head(20).index
    y_test_filtered = [y for y in y_test if y in top_classes]
    y_pred_filtered = [y_pred[i] for i, y in enumerate(y_test) if y in top_classes]
    if y_test_filtered:
        print(classification_report(y_test_filtered, y_pred_filtered, zero_division=0))
    
    # Save model
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\n[SUCCESS] Model saved to: {MODEL_PATH}")
    
    return True, accuracy

if __name__ == "__main__":
    print("=" * 80)
    print("PRODUCT NEED MODEL TRAINING")
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

