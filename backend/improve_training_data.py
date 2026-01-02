"""
Improve training data quality by:
1. Removing exact duplicates
2. Balancing classes
3. Adding more diverse examples for low-accuracy error types
"""

from pathlib import Path
import pandas as pd
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

# Load all training data
ERROR_TEXTS_CSV = DATA_DIR / "error_texts.csv"
REAL_WORLD_CSV = DATA_DIR / "real_world_error_training_data.csv"
SOLUTIONS_CSV = DATA_DIR / "real_world_solutions_training_data.csv"
COMPREHENSIVE_CSV = DATA_DIR / "comprehensive_test_training_data.csv"

def load_and_merge_data():
    """Load and merge all training data sources."""
    dfs = []
    
    if ERROR_TEXTS_CSV.exists():
        df = pd.read_csv(ERROR_TEXTS_CSV)
        if 'text' in df.columns:
            df = df.rename(columns={'text': 'user_text'})
        dfs.append(df)
    
    if REAL_WORLD_CSV.exists():
        df = pd.read_csv(REAL_WORLD_CSV)
        dfs.append(df)
    
    if SOLUTIONS_CSV.exists():
        df = pd.read_csv(SOLUTIONS_CSV)
        dfs.append(df)
    
    if COMPREHENSIVE_CSV.exists():
        df = pd.read_csv(COMPREHENSIVE_CSV)
        dfs.append(df)
    
    if not dfs:
        print("[ERROR] No training data found")
        return None
    
    # Combine
    df_all = pd.concat(dfs, ignore_index=True)
    
    # Clean
    df_all = df_all.dropna(subset=['user_text', 'error_type'])
    df_all['text'] = df_all['user_text'].astype(str).str.lower().str.strip()
    df_all = df_all[df_all['text'].str.len() > 0]
    
    # Remove exact duplicates (same text and error type)
    df_all = df_all.drop_duplicates(subset=['text', 'error_type'])
    
    # Remove near-duplicates (very similar text)
    df_all = df_all.sort_values('text')
    df_all = df_all.drop_duplicates(subset=['text'], keep='first')
    
    print(f"Total samples after deduplication: {len(df_all)}")
    print(f"\nError type distribution:")
    print(df_all['error_type'].value_counts())
    
    return df_all


def balance_classes(df, min_samples_per_class=10, max_samples_per_class=200):
    """Balance classes by sampling."""
    balanced_rows = []
    
    for error_type in df['error_type'].unique():
        class_df = df[df['error_type'] == error_type]
        n_samples = len(class_df)
        
        if n_samples < min_samples_per_class:
            # Keep all if too few
            balanced_rows.append(class_df)
        elif n_samples > max_samples_per_class:
            # Sample if too many
            sampled = class_df.sample(n=max_samples_per_class, random_state=42)
            balanced_rows.append(sampled)
        else:
            # Keep all if in range
            balanced_rows.append(class_df)
    
    df_balanced = pd.concat(balanced_rows, ignore_index=True)
    
    print(f"\nAfter balancing:")
    print(f"Total samples: {len(df_balanced)}")
    print(f"\nError type distribution:")
    print(df_balanced['error_type'].value_counts())
    
    return df_balanced


def main():
    """Main function."""
    print("=" * 80)
    print("IMPROVING TRAINING DATA QUALITY")
    print("=" * 80)
    
    # Load and merge
    df = load_and_merge_data()
    if df is None:
        return
    
    # Balance classes
    df_balanced = balance_classes(df, min_samples_per_class=10, max_samples_per_class=150)
    
    # Save improved training data
    output_file = DATA_DIR / "improved_error_training_data.csv"
    df_balanced.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n{'='*80}")
    print(f"Improved training data saved to: {output_file}")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()

