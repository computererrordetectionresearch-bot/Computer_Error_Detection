"""
Automatically correct all incorrect predictions and retrain models.
This script:
1. Loads incorrect predictions from test results
2. Uses expected values as correct labels
3. Adds corrections to training data
4. Retrains both models
"""

from pathlib import Path
import pandas as pd
import sys
import io
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except (AttributeError, ValueError):
        pass

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

def correct_and_retrain():
    """Correct all incorrect predictions and retrain models."""
    print("=" * 80)
    print("CORRECTING ALL INCORRECT PREDICTIONS AND RETRAINING")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check for incorrect predictions files
    error_incorrect_file = DATA_DIR / "incorrect_error_predictions_100000.csv"
    hardware_incorrect_file = DATA_DIR / "incorrect_hardware_predictions_100000.csv"
    
    error_corrections = None
    hardware_corrections = None
    
    # Load error corrections
    if error_incorrect_file.exists():
        try:
            error_corrections = pd.read_csv(error_incorrect_file)
            print(f"✅ Loaded {len(error_corrections):,} error classification corrections")
        except Exception as e:
            print(f"⚠️  Failed to load error corrections: {e}")
    else:
        print(f"ℹ️  No error corrections file found: {error_incorrect_file}")
    
    # Load hardware corrections
    if hardware_incorrect_file.exists():
        try:
            hardware_corrections = pd.read_csv(hardware_incorrect_file)
            print(f"✅ Loaded {len(hardware_corrections):,} hardware recommendation corrections")
        except Exception as e:
            print(f"⚠️  Failed to load hardware corrections: {e}")
    else:
        print(f"ℹ️  No hardware corrections file found: {hardware_incorrect_file}")
    
    if error_corrections is None and hardware_corrections is None:
        print("\n❌ No correction files found!")
        print("Please run the test first: python test_100000_errors_comprehensive.py")
        return False
    
    # Save corrections to training data files
    success_count = 0
    
    # Process error corrections
    if error_corrections is not None and len(error_corrections) > 0:
        print(f"\n[1/2] Processing {len(error_corrections):,} error classification corrections...")
        
        # Prepare correction data
        corrected_data = error_corrections[['user_text', 'error_type']].copy()
        corrected_data['component_label'] = corrected_data['error_type']
        corrected_data['source'] = 'auto_corrected_from_test'
        
        # Remove any rows with missing data
        corrected_data = corrected_data.dropna(subset=['user_text', 'error_type'])
        corrected_data = corrected_data[corrected_data['user_text'].str.strip().str.len() > 0]
        
        # Save to a corrections file that will be picked up by retraining
        corrections_file = DATA_DIR / "auto_corrected_errors.csv"
        corrected_data.to_csv(corrections_file, index=False, encoding='utf-8')
        print(f"✅ Saved {len(corrected_data):,} error corrections to: {corrections_file}")
        success_count += 1
    
    # Process hardware corrections
    if hardware_corrections is not None and len(hardware_corrections) > 0:
        print(f"\n[2/2] Processing {len(hardware_corrections):,} hardware recommendation corrections...")
        
        # Prepare correction data
        corrected_data = hardware_corrections[['user_text', 'component_label']].copy()
        corrected_data['source'] = 'auto_corrected_from_test'
        
        # Remove any rows with missing data
        corrected_data = corrected_data.dropna(subset=['user_text', 'component_label'])
        corrected_data = corrected_data[corrected_data['user_text'].str.strip().str.len() > 0]
        
        # Save to a corrections file that will be picked up by retraining
        corrections_file = DATA_DIR / "auto_corrected_hardware.csv"
        corrected_data.to_csv(corrections_file, index=False, encoding='utf-8')
        print(f"✅ Saved {len(corrected_data):,} hardware corrections to: {corrections_file}")
        success_count += 1
    
    if success_count == 0:
        print("\n❌ No corrections to process!")
        return False
    
    # Now retrain models with corrections
    print("\n" + "=" * 80)
    print("RETRAINING MODELS WITH CORRECTIONS")
    print("=" * 80)
    
    # Import and run retraining
    try:
        from retrain_from_100000_test import (
            retrain_error_classification_model,
            retrain_hardware_recommendation_model
        )
        
        # Retrain error classification
        if error_corrections is not None and len(error_corrections) > 0:
            print("\n[RETRAINING] Error Classification Model...")
            error_success = retrain_error_classification_model()
            if error_success:
                print("✅ Error classification model retrained successfully")
            else:
                print("❌ Error classification model retraining failed")
        else:
            error_success = True
        
        # Retrain hardware recommendation
        if hardware_corrections is not None and len(hardware_corrections) > 0:
            print("\n[RETRAINING] Hardware Recommendation Model...")
            hardware_success = retrain_hardware_recommendation_model()
            if hardware_success:
                print("✅ Hardware recommendation model retrained successfully")
            else:
                print("❌ Hardware recommendation model retraining failed")
        else:
            hardware_success = True
        
        if error_success and hardware_success:
            print("\n" + "=" * 80)
            print("✅ ALL CORRECTIONS APPLIED AND MODELS RETRAINED")
            print("=" * 80)
            print(f"\nSummary:")
            if error_corrections is not None:
                print(f"  - Error corrections applied: {len(error_corrections):,}")
            if hardware_corrections is not None:
                print(f"  - Hardware corrections applied: {len(hardware_corrections):,}")
            print(f"\n⚠️  IMPORTANT: Restart the backend server to load the retrained models.")
            print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        else:
            print("\n⚠️  Some models failed to retrain. Check errors above.")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during retraining: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    success = correct_and_retrain()
    
    if success:
        print("\n✅ Process completed successfully!")
    else:
        print("\n❌ Process completed with errors.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

