"""
Retrain error classification and hardware recommendation models
using incorrect predictions from 100,000 error test.
"""

from pathlib import Path
import pandas as pd
import joblib
import sys
import io
from datetime import datetime
import shutil
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

# Model paths
ERROR_MODEL_PATH = HERE / "nlp_error_model_error_type.pkl"
HARDWARE_MODEL_PATH = HERE / "product_need_model.pkl"

def backup_model(model_path):
    """Backup existing model before retraining."""
    if model_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = HERE / f"{model_path.stem}_backup_{timestamp}.pkl"
        shutil.copy2(model_path, backup_path)
        print(f"✅ Backed up model to: {backup_path}")
        return backup_path
    return None

def retrain_error_classification_model():
    """Retrain error classification model with corrected data."""
    print("=" * 80)
    print("RETRAINING ERROR CLASSIFICATION MODEL")
    print("=" * 80)
    
    # Backup existing model
    backup_model(ERROR_MODEL_PATH)
    
    # Load all training data sources
    dfs = []
    
    # Original training data
    ERROR_TEXTS_CSV = DATA_DIR / "error_texts.csv"
    if ERROR_TEXTS_CSV.exists():
        df = pd.read_csv(ERROR_TEXTS_CSV)
        if 'text' in df.columns:
            df = df.rename(columns={'text': 'user_text'})
        if 'user_text' in df.columns and 'error_type' in df.columns:
            dfs.append(df[['user_text', 'error_type']])
            print(f"[INFO] Loaded {len(df)} samples from error_texts.csv")
    
    # Improved training data
    IMPROVED_CSV = DATA_DIR / "improved_error_training_data.csv"
    if IMPROVED_CSV.exists():
        df = pd.read_csv(IMPROVED_CSV)
        if 'user_text' in df.columns and 'error_type' in df.columns:
            dfs.append(df[['user_text', 'error_type']])
            print(f"[INFO] Loaded {len(df)} samples from improved_error_training_data.csv")
    
    # Real-world data
    REAL_WORLD_CSV = DATA_DIR / "real_world_error_training_data.csv"
    if REAL_WORLD_CSV.exists():
        df = pd.read_csv(REAL_WORLD_CSV)
        if 'user_text' in df.columns and 'error_type' in df.columns:
            dfs.append(df[['user_text', 'error_type']])
            print(f"[INFO] Loaded {len(df)} samples from real_world_error_training_data.csv")
    
    # Comprehensive test data
    COMPREHENSIVE_CSV = DATA_DIR / "comprehensive_test_training_data.csv"
    if COMPREHENSIVE_CSV.exists():
        df = pd.read_csv(COMPREHENSIVE_CSV)
        if 'user_text' in df.columns and 'error_type' in df.columns:
            dfs.append(df[['user_text', 'error_type']])
            print(f"[INFO] Loaded {len(df)} samples from comprehensive_test_training_data.csv")
    
    # Incorrect predictions from 100,000 test (CORRECTIONS)
    INCORRECT_CSV = DATA_DIR / "incorrect_error_predictions_100000.csv"
    if INCORRECT_CSV.exists():
        df = pd.read_csv(INCORRECT_CSV)
        if 'user_text' in df.columns and 'error_type' in df.columns:
            dfs.append(df[['user_text', 'error_type']])
            print(f"[INFO] Loaded {len(df)} CORRECTED samples from incorrect_error_predictions_100000.csv")
    
    # Auto-corrected errors
    AUTO_CORRECTED_CSV = DATA_DIR / "auto_corrected_errors.csv"
    if AUTO_CORRECTED_CSV.exists():
        df = pd.read_csv(AUTO_CORRECTED_CSV)
        if 'user_text' in df.columns and 'error_type' in df.columns:
            dfs.append(df[['user_text', 'error_type']])
            print(f"[INFO] Loaded {len(df)} AUTO-CORRECTED samples from auto_corrected_errors.csv")
    
    if not dfs:
        print("❌ No training data found!")
        return False
    
    # Combine all data
    df_all = pd.concat(dfs, ignore_index=True)
    df_all = df_all.dropna(subset=['user_text', 'error_type'])
    df_all['user_text'] = df_all['user_text'].astype(str).str.strip()
    df_all = df_all[df_all['user_text'].str.len() > 0]
    
    # Remove duplicates
    df_all = df_all.drop_duplicates(subset=['user_text', 'error_type'])
    
    # Filter out classes with only 1 sample (they can't be properly evaluated)
    class_counts = df_all['error_type'].value_counts()
    classes_to_keep = class_counts[class_counts >= 2].index
    df_all = df_all[df_all['error_type'].isin(classes_to_keep)]
    
    if len(class_counts[class_counts < 2]) > 0:
        print(f"\n[INFO] Filtered out {len(class_counts[class_counts < 2])} error types with < 2 samples")
        print(f"[INFO] Removed types: {list(class_counts[class_counts < 2].index)}")
    
    print(f"\n[INFO] Total training samples: {len(df_all)}")
    print(f"[INFO] Error types: {df_all['error_type'].nunique()}")
    print(f"\nError type distribution:")
    print(df_all['error_type'].value_counts().head(15))
    
    # Prepare data
    X = df_all['user_text'].values
    y = df_all['error_type'].values
    
    # Split data (now all classes have at least 2 samples, so stratified split is safe)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n[INFO] Training samples: {len(X_train)}")
    print(f"[INFO] Test samples: {len(X_test)}")
    
    # Create pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=10000,
            min_df=2,
            max_df=0.95
        )),
        ('classifier', SGDClassifier(
            loss='log_loss',
            alpha=0.0001,
            max_iter=1000,
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
    joblib.dump(pipeline, ERROR_MODEL_PATH)
    print(f"\n✅ Model saved to: {ERROR_MODEL_PATH}")
    
    return True

def retrain_hardware_recommendation_model():
    """Retrain hardware recommendation model with corrected data."""
    print("\n" + "=" * 80)
    print("RETRAINING HARDWARE RECOMMENDATION MODEL")
    print("=" * 80)
    
    # Backup existing model
    backup_model(HARDWARE_MODEL_PATH)
    
    # Load all training data sources
    dfs = []
    
    # Original hardware data
    HARDWARE_CSV = DATA_DIR / "hardware_component_dataset_merged.csv"
    if HARDWARE_CSV.exists():
        df = pd.read_csv(HARDWARE_CSV)
        if 'user_text' in df.columns and 'component_label' in df.columns:
            dfs.append(df[['user_text', 'component_label']])
            print(f"[INFO] Loaded {len(df)} samples from hardware_component_dataset_merged.csv")
    
    # Improved hardware data
    HARDWARE_IMPROVED_CSV = DATA_DIR / "hardware_component_dataset_improved.csv"
    if HARDWARE_IMPROVED_CSV.exists():
        df = pd.read_csv(HARDWARE_IMPROVED_CSV)
        if 'user_text' in df.columns and 'component_label' in df.columns:
            dfs.append(df[['user_text', 'component_label']])
            print(f"[INFO] Loaded {len(df)} samples from hardware_component_dataset_improved.csv")
    
    # Incorrect hardware predictions from 100,000 test (CORRECTIONS)
    INCORRECT_HARDWARE_CSV = DATA_DIR / "incorrect_hardware_predictions_100000.csv"
    if INCORRECT_HARDWARE_CSV.exists():
        df = pd.read_csv(INCORRECT_HARDWARE_CSV)
        if 'user_text' in df.columns and 'component_label' in df.columns:
            dfs.append(df[['user_text', 'component_label']])
            print(f"[INFO] Loaded {len(df)} CORRECTED samples from incorrect_hardware_predictions_100000.csv")
    
    # Auto-corrected hardware
    AUTO_CORRECTED_HARDWARE_CSV = DATA_DIR / "auto_corrected_hardware.csv"
    if AUTO_CORRECTED_HARDWARE_CSV.exists():
        df = pd.read_csv(AUTO_CORRECTED_HARDWARE_CSV)
        if 'user_text' in df.columns and 'component_label' in df.columns:
            dfs.append(df[['user_text', 'component_label']])
            print(f"[INFO] Loaded {len(df)} AUTO-CORRECTED samples from auto_corrected_hardware.csv")
    
    # Product need feedback
    FEEDBACK_CSV = DATA_DIR / "product_need_feedback.csv"
    if FEEDBACK_CSV.exists():
        df = pd.read_csv(FEEDBACK_CSV)
        if 'user_text' in df.columns and 'user_correct_label' in df.columns:
            df_feedback = df[df['user_correct_label'].notna()][['user_text', 'user_correct_label']]
            df_feedback = df_feedback.rename(columns={'user_correct_label': 'component_label'})
            dfs.append(df_feedback)
            print(f"[INFO] Loaded {len(df_feedback)} samples from product_need_feedback.csv")
    
    if not dfs:
        print("❌ No training data found!")
        return False
    
    # Combine all data
    df_all = pd.concat(dfs, ignore_index=True)
    df_all = df_all.dropna(subset=['user_text', 'component_label'])
    df_all['user_text'] = df_all['user_text'].astype(str).str.strip()
    df_all = df_all[df_all['user_text'].str.len() > 0]
    
    # Remove duplicates
    df_all = df_all.drop_duplicates(subset=['user_text', 'component_label'])
    
    # Filter out classes with only 1 sample (they can't be properly evaluated)
    class_counts = df_all['component_label'].value_counts()
    classes_to_keep = class_counts[class_counts >= 2].index
    df_all = df_all[df_all['component_label'].isin(classes_to_keep)]
    
    if len(class_counts[class_counts < 2]) > 0:
        removed_count = len(class_counts[class_counts < 2])
        print(f"\n[INFO] Filtered out {removed_count} component types with < 2 samples")
        removed_types = list(class_counts[class_counts < 2].index)
        if removed_count <= 10:
            print(f"[INFO] Removed types: {removed_types}")
        else:
            print(f"[INFO] Removed types (first 10): {removed_types[:10]}...")
            print(f"[INFO] ... and {removed_count - 10} more")
    
    print(f"\n[INFO] Total training samples: {len(df_all)}")
    print(f"[INFO] Component types: {df_all['component_label'].nunique()}")
    print(f"\nComponent distribution (top 15):")
    print(df_all['component_label'].value_counts().head(15))
    
    # Prepare data
    X = df_all['user_text'].values
    y = df_all['component_label'].values
    
    # Split data (now all classes have at least 2 samples, so stratified split is safe)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n[INFO] Training samples: {len(X_train)}")
    print(f"[INFO] Test samples: {len(X_test)}")
    
    # Create pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=15000,
            min_df=2,
            max_df=0.95
        )),
        ('classifier', SGDClassifier(
            loss='log_loss',
            alpha=0.0001,
            max_iter=1000,
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
    
    # Save model
    joblib.dump(pipeline, HARDWARE_MODEL_PATH)
    print(f"\n✅ Model saved to: {HARDWARE_MODEL_PATH}")
    
    return True

def main():
    """Main retraining function."""
    print("=" * 80)
    print("RETRAINING MODELS FROM 100,000 ERROR TEST CORRECTIONS")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Retrain error classification
    error_success = retrain_error_classification_model()
    
    # Retrain hardware recommendation
    hardware_success = retrain_hardware_recommendation_model()
    
    print("\n" + "=" * 80)
    print("RETRAINING SUMMARY")
    print("=" * 80)
    print(f"Error Classification Model: {'✅ Success' if error_success else '❌ Failed'}")
    print(f"Hardware Recommendation Model: {'✅ Success' if hardware_success else '❌ Failed'}")
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    if error_success and hardware_success:
        print("\n✅ Both models retrained successfully!")
        print("⚠️  Please restart the backend server to load the new models.")
    else:
        print("\n⚠️  Some models failed to retrain. Check the errors above.")

if __name__ == "__main__":
    main()

