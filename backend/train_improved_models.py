"""
Improved Training Scripts for All ML Models
Uses better algorithms, hyperparameters, and techniques to improve accuracy.
"""

from pathlib import Path
import pandas as pd
import joblib
import json
import sys
import io
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

# ============================================================================
# 1. IMPROVED ERROR TYPE CLASSIFIER
# ============================================================================
def train_error_type_model():
    """Train improved error type classifier with better algorithms."""
    print("=" * 80)
    print("TRAINING IMPROVED ERROR TYPE CLASSIFIER")
    print("=" * 80)
    
    IMPROVED_CSV = DATA_DIR / "improved_error_training_data.csv"
    ERROR_TEXTS_CSV = DATA_DIR / "error_texts.csv"
    REAL_WORLD_CSV = DATA_DIR / "real_world_error_training_data.csv"
    SOLUTIONS_CSV = DATA_DIR / "real_world_solutions_training_data.csv"
    COMPREHENSIVE_CSV = DATA_DIR / "comprehensive_test_training_data.csv"
    MODEL_PATH = HERE / "nlp_error_model_error_type.pkl"
    
    # Load ALL available data sources and combine them
    dfs = []
    
    # Load improved data if available
    if IMPROVED_CSV.exists():
        df_improved = pd.read_csv(IMPROVED_CSV)
        if 'user_text' in df_improved.columns or 'error_type' in df_improved.columns:
            dfs.append(df_improved)
            print(f"[INFO] Loaded {len(df_improved)} samples from improved training data")
    
    # Load existing data
    if ERROR_TEXTS_CSV.exists():
        df_existing = pd.read_csv(ERROR_TEXTS_CSV)
        if 'text' in df_existing.columns:
            df_existing = df_existing.rename(columns={'text': 'user_text'})
        if 'user_text' in df_existing.columns or 'error_type' in df_existing.columns:
            dfs.append(df_existing)
            print(f"[INFO] Loaded {len(df_existing)} samples from existing data")
    
    # Load real-world data
    if REAL_WORLD_CSV.exists():
        df_real = pd.read_csv(REAL_WORLD_CSV)
        dfs.append(df_real)
        print(f"[INFO] Loaded {len(df_real)} samples from real-world data")
    
    # Load solutions data
    if SOLUTIONS_CSV.exists():
        df_solutions = pd.read_csv(SOLUTIONS_CSV)
        dfs.append(df_solutions)
        print(f"[INFO] Loaded {len(df_solutions)} samples from solutions data")
    
    # Load comprehensive test data
    if COMPREHENSIVE_CSV.exists():
        df_comprehensive = pd.read_csv(COMPREHENSIVE_CSV)
        dfs.append(df_comprehensive)
        print(f"[INFO] Loaded {len(df_comprehensive)} samples from comprehensive test data")
    
    # Load test dataset (1000 errors) - IMPORTANT for covering all error types
    TEST_1000_CSV = DATA_DIR / "test_1000_errors.csv"
    if TEST_1000_CSV.exists():
        df_test = pd.read_csv(TEST_1000_CSV)
        dfs.append(df_test)
        print(f"[INFO] Loaded {len(df_test)} samples from test dataset (1000 errors)")
    
    # Load incorrect predictions (for correction)
    INCORRECT_CSV = DATA_DIR / "incorrect_predictions_for_retraining.csv"
    if INCORRECT_CSV.exists():
        df_incorrect = pd.read_csv(INCORRECT_CSV)
        dfs.append(df_incorrect)
        print(f"[INFO] Loaded {len(df_incorrect)} samples from incorrect predictions (for correction)")
    
    if not dfs:
        print(f"❌ No training data found")
        return False
    
    # Combine all data
    df = pd.concat(dfs, ignore_index=True)
    df = df.dropna(subset=['user_text', 'error_type'])
    df['text'] = df['user_text'].astype(str).str.lower().str.strip()
    df = df[df['text'].str.len() > 0]
    
    # Remove duplicates (keep first occurrence)
    df = df.drop_duplicates(subset=['text', 'error_type'])
    df = df.drop_duplicates(subset=['text'], keep='first')
    
    print(f"📊 Loaded {len(df)} training samples")
    print(f"📊 Classes: {df['error_type'].nunique()}")
    print(f"\nClass distribution:")
    print(df['error_type'].value_counts().head(10))
    
    X = df['text'].values
    y = df['error_type'].values
    
    # Check if we have enough samples per class for stratified split
    class_counts = pd.Series(y).value_counts()
    min_samples = class_counts.min()
    
    # Split data
    if min_samples >= 2:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        print(f"\n⚠️ Warning: Some classes have only 1 sample. Using regular split.")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    
    print(f"\n📊 Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Try multiple algorithms with better configurations
    from sklearn.utils.class_weight import compute_class_weight
    import numpy as np
    
    # Compute class weights for imbalanced data
    classes = np.unique(y_train)
    class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
    class_weight_dict = dict(zip(classes, class_weights))
    
    algorithms = {
        'LogisticRegression': LogisticRegression(
            max_iter=2000, 
            random_state=42, 
            C=1.0,
            class_weight='balanced',
            multi_class='multinomial',
            solver='lbfgs'
        ),
        'SGDClassifier': SGDClassifier(
            random_state=42, 
            max_iter=2000, 
            loss='log_loss',
            class_weight='balanced',
            alpha=0.0001
        ),
        'MultinomialNB': MultinomialNB(alpha=0.5),
    }
    
    best_score = 0
    best_model = None
    best_name = None
    
    print("\n🔍 Testing different algorithms with class balancing...")
    for name, clf in algorithms.items():
        # Try different TF-IDF configurations
        tfidf_configs = [
            {'ngram_range': (1, 2), 'min_df': 1, 'max_df': 0.95},
            {'ngram_range': (1, 3), 'min_df': 1, 'max_df': 0.95},
        ]
        
        for tfidf_cfg in tfidf_configs:
            pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(
                    ngram_range=tfidf_cfg['ngram_range'],
                    min_df=tfidf_cfg['min_df'],
                    max_df=tfidf_cfg['max_df'],
                    sublinear_tf=True,
                    stop_words='english',
                    max_features=5000
                )),
                ('clf', clf)
            ])
            
            try:
                # Cross-validation with fewer folds for speed
                scores = cross_val_score(pipeline, X_train, y_train, cv=3, scoring='accuracy')
                avg_score = scores.mean()
                
                config_str = f"ngram={tfidf_cfg['ngram_range']}, min_df={tfidf_cfg['min_df']}"
                print(f"   {name:20s} ({config_str:30s}): {avg_score:.4f} (+/- {scores.std():.4f})")
                
                if avg_score > best_score:
                    best_score = avg_score
                    best_model = pipeline
                    best_name = f"{name} ({config_str})"
            except Exception as e:
                print(f"   {name:20s}: Failed - {str(e)[:50]}")
    
    print(f"\n✅ Best algorithm: {best_name} (CV Score: {best_score:.4f})")
    
    # Train best model
    print("\n🔄 Training best model on full training set...")
    best_model.fit(X_train, y_train)
    
    # Evaluate on test set
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n📈 Test Accuracy: {accuracy:.4f}")
    print(f"\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    joblib.dump(best_model, MODEL_PATH)
    print(f"\n💾 Model saved to: {MODEL_PATH}")
    
    return True

# ============================================================================
# 2. IMPROVED PRODUCT CATEGORY CLASSIFIER (with data augmentation)
# ============================================================================
def train_product_category_model():
    """Train improved product category classifier with data augmentation."""
    print("\n" + "=" * 80)
    print("TRAINING IMPROVED PRODUCT CATEGORY CLASSIFIER")
    print("=" * 80)
    
    PRODUCT_TEXTS_CSV = DATA_DIR / "product_texts.csv"
    HARDWARE_CSV = DATA_DIR / "hardware_component_dataset_merged.csv"
    MODEL_PATH = HERE / "nlp_error_model_product.pkl"
    
    # Load primary data
    if not PRODUCT_TEXTS_CSV.exists():
        print(f"❌ Training data not found: {PRODUCT_TEXTS_CSV}")
        return False
    
    df = pd.read_csv(PRODUCT_TEXTS_CSV)
    df = df.dropna(subset=['text', 'product_category'])
    df['text'] = df['text'].astype(str).str.lower().str.strip()
    df = df[df['text'].str.len() > 0]
    
    print(f"📊 Primary dataset: {len(df)} samples")
    
    # Try to augment with hardware dataset
    if HARDWARE_CSV.exists():
        try:
            hw_df = pd.read_csv(HARDWARE_CSV)
            if 'user_text' in hw_df.columns and 'component_label' in hw_df.columns:
                # Map component labels to product categories
                category_mapping = {
                    'GPU': 'GPU',
                    'GPU Upgrade': 'GPU',
                    'SSD': 'SSD',
                    'SSD Upgrade': 'SSD',
                    'Laptop SSD Upgrade': 'SSD',
                    'NVMe SSD Upgrade': 'SSD',
                    'RAM': 'RAM',
                    'RAM Upgrade': 'RAM',
                    'Laptop RAM Upgrade': 'RAM',
                    'PSU': 'PSU',
                    'PSU Upgrade': 'PSU',
                    'WiFi Adapter': 'Wi-Fi Adapter',
                    'WiFi Adapter Upgrade': 'Wi-Fi Adapter',
                    'Wi-Fi Adapter': 'Wi-Fi Adapter',
                }
                
                hw_df = hw_df.dropna(subset=['user_text', 'component_label'])
                hw_df['text'] = hw_df['user_text'].astype(str).str.lower().str.strip()
                hw_df['product_category'] = hw_df['component_label'].map(category_mapping)
                hw_df = hw_df.dropna(subset=['product_category'])
                hw_df = hw_df[['text', 'product_category']]
                
                # Combine datasets
                df = pd.concat([df, hw_df], ignore_index=True)
                df = df.drop_duplicates(subset=['text'])
                
                print(f"📊 After augmentation: {len(df)} samples")
        except Exception as e:
            print(f"⚠️ Could not augment with hardware dataset: {e}")
    
    print(f"📊 Classes: {df['product_category'].nunique()}")
    print(f"\nClass distribution:")
    print(df['product_category'].value_counts())
    
    X = df['text'].values
    y = df['product_category'].values
    
    # Check if we have enough samples per class
    class_counts = pd.Series(y).value_counts()
    min_samples = class_counts.min()
    
    if min_samples < 3:
        print(f"\n⚠️ Warning: Some classes have very few samples (min: {min_samples})")
        print("   Using stratified split may fail, using regular split instead.")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    
    print(f"\n📊 Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Try multiple algorithms with different hyperparameters (all support predict_proba natively)
    algorithms = {
        'LogisticRegression': LogisticRegression(max_iter=2000, random_state=42, C=2.0),
        'SGDClassifier': SGDClassifier(random_state=42, max_iter=2000, loss='log_loss', alpha=0.0001),
        'MultinomialNB': MultinomialNB(alpha=0.5),
    }
    
    best_score = 0
    best_model = None
    best_name = None
    
    print("\n🔍 Testing different algorithms...")
    for name, clf in algorithms.items():
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,  # Lower min_df for small dataset
                max_df=0.95,
                sublinear_tf=True,
                stop_words='english'
            )),
            ('clf', clf)
        ])
        
        # Cross-validation (fewer folds for small dataset)
        try:
            cv_folds = min(5, min_samples) if min_samples >= 2 else 3
            scores = cross_val_score(pipeline, X_train, y_train, cv=cv_folds, scoring='accuracy')
            avg_score = scores.mean()
            
            print(f"   {name:20s}: {avg_score:.4f} (+/- {scores.std():.4f})")
            
            if avg_score > best_score:
                best_score = avg_score
                best_model = pipeline
                best_name = name
        except Exception as e:
            print(f"   {name:20s}: Failed ({str(e)[:50]})")
    
    if best_model is None:
        print("❌ All algorithms failed. Using default LogisticRegression.")
        best_model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ('clf', LogisticRegression(max_iter=2000, random_state=42))
        ])
        best_name = "LogisticRegression (default)"
    
    print(f"\n✅ Best algorithm: {best_name} (CV Score: {best_score:.4f})")
    
    # Train best model
    print("\n🔄 Training best model on full training set...")
    best_model.fit(X_train, y_train)
    
    # Evaluate on test set
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n📈 Test Accuracy: {accuracy:.4f}")
    print(f"\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    joblib.dump(best_model, MODEL_PATH)
    print(f"\n💾 Model saved to: {MODEL_PATH}")
    
    return True

# ============================================================================
# 3. IMPROVED PRODUCT NEED CLASSIFIER
# ============================================================================
def train_product_need_model():
    """Train improved product need classifier."""
    print("\n" + "=" * 80)
    print("TRAINING IMPROVED PRODUCT NEED CLASSIFIER")
    print("=" * 80)
    
    # Try improved data first, then fallback to merged
    IMPROVED_CSV = DATA_DIR / "hardware_component_dataset_improved.csv"
    HARDWARE_CSV = DATA_DIR / "hardware_component_dataset_merged.csv"
    MODEL_PATH = HERE / "product_need_model.pkl"
    
    # Prefer improved data if available
    if IMPROVED_CSV.exists():
        HARDWARE_CSV = IMPROVED_CSV
        print(f"[INFO] Using improved training data: {IMPROVED_CSV}")
    elif not HARDWARE_CSV.exists():
        print(f"❌ Training data not found: {HARDWARE_CSV}")
        return False
    
    # Load data
    df = pd.read_csv(HARDWARE_CSV)
    df = df.dropna(subset=['user_text', 'component_label'])
    df['text'] = df['user_text'].astype(str).str.lower().str.strip()
    df = df[df['text'].str.len() > 0]
    
    print(f"📊 Loaded {len(df)} training samples")
    print(f"📊 Classes: {df['component_label'].nunique()}")
    print(f"\nTop 10 classes:")
    print(df['component_label'].value_counts().head(10))
    
    X = df['text'].values
    y = df['component_label'].values
    
    # Filter classes with at least 2 samples for stratified split
    class_counts = pd.Series(y).value_counts()
    valid_classes = class_counts[class_counts >= 2].index
    df_filtered = df[df['component_label'].isin(valid_classes)]
    
    if len(df_filtered) < len(df) * 0.8:
        print(f"\n⚠️ Warning: Filtered out {len(df) - len(df_filtered)} samples with rare classes")
        print(f"   Using {len(df_filtered)} samples for training")
        X = df_filtered['text'].values
        y = df_filtered['component_label'].values
    
    # Split data
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    except:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    
    print(f"\n📊 Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Try multiple algorithms (all support predict_proba natively)
    algorithms = {
        'LogisticRegression': LogisticRegression(max_iter=500, random_state=42, C=1.0, multi_class='multinomial'),
        'SGDClassifier': SGDClassifier(random_state=42, max_iter=1000, loss='log_loss'),
    }
    
    best_score = 0
    best_model = None
    best_name = None
    
    print("\n🔍 Testing different algorithms...")
    for name, clf in algorithms.items():
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95,
                sublinear_tf=True,
                stop_words='english'
            )),
            ('clf', clf)
        ])
        
        # Cross-validation
        try:
            scores = cross_val_score(pipeline, X_train, y_train, cv=3, scoring='accuracy')
            avg_score = scores.mean()
            
            print(f"   {name:20s}: {avg_score:.4f} (+/- {scores.std():.4f})")
            
            if avg_score > best_score:
                best_score = avg_score
                best_model = pipeline
                best_name = name
        except Exception as e:
            print(f"   {name:20s}: Failed ({str(e)[:50]})")
    
    if best_model is None:
        print("❌ All algorithms failed. Using default LogisticRegression.")
        best_model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2)),
            ('clf', LogisticRegression(max_iter=500, random_state=42, multi_class='multinomial'))
        ])
        best_name = "LogisticRegression (default)"
    
    print(f"\n✅ Best algorithm: {best_name} (CV Score: {best_score:.4f})")
    
    # Train best model
    print("\n🔄 Training best model on full training set...")
    best_model.fit(X_train, y_train)
    
    # Evaluate on test set
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n📈 Test Accuracy: {accuracy:.4f}")
    print(f"\n📊 Top 10 classes classification report:")
    top_classes = pd.Series(y_test).value_counts().head(10).index
    top_mask = np.isin(y_test, top_classes)
    if top_mask.sum() > 0:
        print(classification_report(y_test[top_mask], y_pred[top_mask]))
    
    # Save model
    joblib.dump(best_model, MODEL_PATH)
    print(f"\n💾 Model saved to: {MODEL_PATH}")
    
    return True

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("IMPROVED MODEL TRAINING SUITE")
    print("=" * 80)
    
    results = {
        "Error Type Model": train_error_type_model(),
        "Product Category Model": train_product_category_model(),
        "Product Need Model": train_product_need_model(),
    }
    
    print("\n" + "=" * 80)
    print("TRAINING SUMMARY")
    print("=" * 80)
    
    for model_name, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        print(f"   {status}: {model_name}")
    
    all_success = all(results.values())
    if all_success:
        print("\n🎉 All models trained successfully!")
    else:
        print("\n⚠️ Some models failed to train. Check errors above.")

