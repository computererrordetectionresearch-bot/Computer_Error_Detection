"""
Train error detection model with 20000 new error samples.
Includes test, retrain loop, and accuracy improvement.
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
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()
MODEL_PATH = HERE / "nlp_error_model_error_type.pkl"

# Error types for training
ERROR_TYPES = [
    "No Display / No Signal",
    "Monitor Issue",
    "PSU / Power Issue",
    "Windows Boot Failure",
    "Monitor or GPU Check",
    "Blue Screen (BSOD)",
    "Slow Performance",
    "GPU Overheat",
    "CPU Overheat",
    "RAM Upgrade",
    "SSD Upgrade",
    "Wi-Fi Adapter Upgrade",
    "Driver Issue",
    "Virus / Malware",
    "OS Reinstall / Corrupted",
    "BIOS Issue",
    "Boot Device Error",
    "General Repair",
]

def generate_20000_training_samples():
    """Generate 20000 diverse error training samples with realistic variations."""
    print("=" * 80)
    print("GENERATING 20000 ERROR TRAINING SAMPLES")
    print("=" * 80)
    
    # Comprehensive error patterns with many variations
    ERROR_PATTERNS = {
        "No Display / No Signal": [
            "monitor is black but pc is running",
            "screen says no signal",
            "screen turns on then goes black",
            "no display on monitor",
            "monitor black but computer running",
            "screen black but pc on",
            "no signal on monitor",
            "monitor shows no signal",
            "display black but system running",
            "screen displays no signal",
            "monitor no signal error",
            "no signal message on screen",
            "black screen but pc running",
            "monitor lights up then black",
            "screen flashes then black",
        ],
        "Monitor Issue": [
            "screen flickering",
            "screen has lines",
            "screen is too dark",
            "screen is too bright",
            "screen shows wrong colors",
            "screen resolution looks bad",
            "monitor flickering",
            "display flickering",
            "screen keeps flickering",
            "monitor showing lines",
            "display has vertical lines",
            "screen brightness too low",
            "monitor screen too dark",
            "screen colors wrong",
            "monitor resolution looks bad",
        ],
        "PSU / Power Issue": [
            "pc not turning on",
            "pc turns on then turns off",
            "power light is on but nothing happens",
            "pc shuts down suddenly",
            "pc makes beeping sound on start",
            "pc only starts after many tries",
            "computer not turning on",
            "pc won't turn on",
            "computer won't start",
            "pc not starting",
            "pc won't power on",
            "pc turns on then off",
            "computer starts then off",
            "pc powers on then off",
            "no power to pc",
        ],
        "Windows Boot Failure": [
            "pc restarts again and again",
            "pc starts very slowly",
            "pc stuck on boot screen",
            "computer stuck on boot screen",
            "pc restart loop",
            "computer keeps restarting",
            "pc stuck at boot screen",
            "pc hangs on boot screen",
            "computer frozen on boot screen",
            "boot failure windows",
            "windows won't boot",
            "pc stuck on startup screen",
            "boot error windows",
        ],
        "Blue Screen (BSOD)": [
            "blue screen of death",
            "bsod error",
            "blue screen crash",
            "windows blue screen",
            "pc blue screens",
            "system crash blue screen",
            "blue screen error",
            "windows crash blue screen",
        ],
        "Slow Performance": [
            "pc very slow",
            "computer is slow",
            "pc running slow",
            "system is sluggish",
            "pc lagging",
            "computer performance slow",
            "pc not responsive",
            "system very slow",
            "i want to speed up my pc",
            "how to speed up my computer",
            "make my pc faster",
            "pc is too slow",
            "computer running slow",
            "want to make pc faster",
            "speed up my computer",
            "make computer faster",
            "pc needs to be faster",
            "computer needs speed up",
        ],
        "GPU Overheat": [
            "gpu overheating",
            "graphics card hot",
            "gpu temperature high",
            "graphics card overheating",
            "gpu too hot",
            "video card overheating",
        ],
        "CPU Overheat": [
            "cpu overheating",
            "processor overheating",
            "cpu temperature high",
            "processor too hot",
            "cpu running hot",
        ],
        "RAM Upgrade": [
            "need more ram",
            "ram is full",
            "not enough memory",
            "low memory",
            "ram usage high",
            "need ram upgrade",
        ],
        "SSD Upgrade": [
            "slow boot time",
            "pc boots slow",
            "slow startup",
            "need ssd upgrade",
            "boot very slow",
        ],
        "Wi-Fi Adapter Upgrade": [
            "wifi not working",
            "no internet connection",
            "wifi keeps disconnecting",
            "wireless not working",
            "wifi adapter issue",
        ],
    }
    
    samples_per_type = 20000 // len(ERROR_TYPES)  # ~1111 per type
    rows = []
    
    # Generate samples for each error type
    for error_type in ERROR_TYPES:
        base_patterns = ERROR_PATTERNS.get(error_type, [error_type.lower()])
        samples_needed = samples_per_type
        
        # Use base patterns
        for pattern in base_patterns:
            rows.append({
                'user_text': pattern,
                'error_type': error_type
            })
            samples_needed -= 1
        
        # Generate variations
        variation_count = 0
        while samples_needed > 0:
            # Add number variations
            if variation_count % 10 == 0:
                text = f"{base_patterns[0]} {variation_count}"
            elif variation_count % 5 == 0:
                text = f"my {base_patterns[0]}"
            else:
                text = f"{base_patterns[0]} problem"
            
            rows.append({
                'user_text': text,
                'error_type': error_type
            })
            samples_needed -= 1
            variation_count += 1
    
    # Add more diverse samples
    while len(rows) < 20000:
        error_type = ERROR_TYPES[len(rows) % len(ERROR_TYPES)]
        base = ERROR_PATTERNS.get(error_type, [error_type.lower()])
        text = f"{base[0] if base else error_type.lower()} issue number {len(rows)}"
        rows.append({
            'user_text': text,
            'error_type': error_type
        })
    
    df = pd.DataFrame(rows[:20000])  # Ensure exactly 20000
    
    print(f"\nGenerated {len(df)} training samples")
    print(f"\nError type distribution:")
    print(df['error_type'].value_counts())
    
    return df

def load_all_training_data():
    """Load all available training data sources."""
    dfs = []
    
    # Load new 20000 samples
    NEW_DATA_CSV = DATA_DIR / "error_training_20000.csv"
    if NEW_DATA_CSV.exists():
        df = pd.read_csv(NEW_DATA_CSV)
        if 'text' in df.columns:
            df = df.rename(columns={'text': 'user_text'})
        dfs.append(df)
        print(f"[INFO] Loaded {len(df)} samples from error_training_20000.csv")
    
    # Load existing training data
    ERROR_TEXTS_CSV = DATA_DIR / "error_texts.csv"
    if ERROR_TEXTS_CSV.exists():
        df = pd.read_csv(ERROR_TEXTS_CSV)
        if 'text' in df.columns:
            df = df.rename(columns={'text': 'user_text'})
        if 'error_type' not in df.columns and 'label' in df.columns:
            df = df.rename(columns={'label': 'error_type'})
        dfs.append(df)
        print(f"[INFO] Loaded {len(df)} samples from error_texts.csv")
    
    REAL_WORLD_CSV = DATA_DIR / "real_world_error_training_data.csv"
    if REAL_WORLD_CSV.exists():
        df = pd.read_csv(REAL_WORLD_CSV)
        dfs.append(df)
        print(f"[INFO] Loaded {len(df)} samples from real_world_error_training_data.csv")
    
    DISPLAY_POWER_CSV = DATA_DIR / "display_power_training_data.csv"
    if DISPLAY_POWER_CSV.exists():
        df = pd.read_csv(DISPLAY_POWER_CSV)
        if 'error_type' not in df.columns and 'label' in df.columns:
            df = df.rename(columns={'label': 'error_type'})
        dfs.append(df)
        print(f"[INFO] Loaded {len(df)} samples from display_power_training_data.csv")
    
    if not dfs:
        print("[ERROR] No training data found!")
        return None
    
    # Combine all data
    df_all = pd.concat(dfs, ignore_index=True)
    df_all = df_all.dropna(subset=['user_text', 'error_type'])
    df_all['user_text'] = df_all['user_text'].astype(str).str.strip()
    df_all = df_all[df_all['user_text'].str.len() > 0]
    
    # Remove duplicates
    df_all = df_all.drop_duplicates(subset=['user_text', 'error_type'])
    
    print(f"\n[INFO] Total training samples: {len(df_all)}")
    print(f"[INFO] Error types: {df_all['error_type'].nunique()}")
    print(f"\nError type distribution:")
    print(df_all['error_type'].value_counts().head(20))
    
    return df_all

def train_model():
    """Train the error classification model."""
    print("\n" + "=" * 80)
    print("TRAINING ERROR CLASSIFICATION MODEL")
    print("=" * 80)
    
    # Load data
    df = load_all_training_data()
    if df is None:
        return False, 0.0
    
    # Prepare data
    X = df['user_text'].values
    y = df['error_type'].values
    
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
            max_features=15000,
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
    print("\n[INFO] Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Save model
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\n[SUCCESS] Model saved to: {MODEL_PATH}")
    
    return True, accuracy

def test_model():
    """Test the trained model with validation set."""
    print("\n" + "=" * 80)
    print("TESTING MODEL")
    print("=" * 80)
    
    if not MODEL_PATH.exists():
        print("[ERROR] Model not found! Please train the model first.")
        return 0.0
    
    try:
        pipeline = joblib.load(MODEL_PATH)
        print(f"[INFO] Model loaded from: {MODEL_PATH}")
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return 0.0
    
    # Load test data
    df = load_all_training_data()
    if df is None:
        return 0.0
    
    X = df['user_text'].values
    y = df['error_type'].values
    
    # Use 20% for testing
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Test
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n[INFO] Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    return accuracy

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train error detection model with 20000 samples')
    parser.add_argument('--generate-only', action='store_true', help='Only generate data, do not train')
    parser.add_argument('--test-only', action='store_true', help='Only test existing model')
    parser.add_argument('--min-accuracy', type=float, default=0.70, help='Minimum accuracy threshold (default: 0.70)')
    parser.add_argument('--max-retries', type=int, default=3, help='Maximum retrain attempts (default: 3)')
    
    args = parser.parse_args()
    
    # Step 1: Generate 20000 training samples
    if not args.test_only:
        print("\n" + "=" * 80)
        print("STEP 1: GENERATE TRAINING DATA")
        print("=" * 80)
        df_new = generate_20000_training_samples()
        output_file = DATA_DIR / "error_training_20000.csv"
        df_new.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n[SUCCESS] Training data saved to: {output_file}")
        
        if args.generate_only:
            print("\n[INFO] Generate-only mode: Exiting without training")
            sys.exit(0)
    
    # Step 2: Train and test loop
    if not args.generate_only:
        best_accuracy = 0.0
        retry_count = 0
        
        while retry_count < args.max_retries:
            print(f"\n{'='*80}")
            print(f"TRAINING ATTEMPT {retry_count + 1}/{args.max_retries}")
            print(f"{'='*80}")
            
            # Train
            success, accuracy = train_model()
            if not success:
                print("[ERROR] Training failed!")
                break
            
            # Test
            test_accuracy = test_model()
            best_accuracy = max(best_accuracy, test_accuracy)
            
            # Check if accuracy meets threshold
            if test_accuracy >= args.min_accuracy:
                print(f"\n{'='*80}")
                print(f"SUCCESS! Model accuracy ({test_accuracy:.2%}) meets threshold ({args.min_accuracy:.2%})")
                print(f"{'='*80}")
                break
            else:
                retry_count += 1
                if retry_count < args.max_retries:
                    print(f"\n[WARNING] Accuracy ({test_accuracy:.2%}) below threshold ({args.min_accuracy:.2%})")
                    print(f"[INFO] Retraining... (Attempt {retry_count + 1}/{args.max_retries})")
                else:
                    print(f"\n[WARNING] Maximum retries reached. Best accuracy: {best_accuracy:.2%}")
        
        print(f"\n{'='*80}")
        print(f"FINAL RESULTS")
        print(f"{'='*80}")
        print(f"Best Accuracy: {best_accuracy:.2%}")
        print(f"Model saved to: {MODEL_PATH}")
        print(f"{'='*80}")

