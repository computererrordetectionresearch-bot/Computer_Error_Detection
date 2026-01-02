"""
Comprehensive test script for 100,000 PC errors.
Tests both error classification and hardware recommendation accuracy.
Identifies incorrect predictions for retraining.
"""

from pathlib import Path
import pandas as pd
import sys
import io
import json
import os
from collections import defaultdict
from datetime import datetime
import traceback
from contextlib import redirect_stdout, redirect_stderr

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except (AttributeError, ValueError):
        # stdout might already be wrapped or closed
        pass

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()
TEST_CSV = DATA_DIR / "test_100000_errors.csv"

def test_error_classification():
    """Test error type classification accuracy."""
    print("=" * 80)
    print("TESTING ERROR CLASSIFICATION")
    print("=" * 80)
    
    if not TEST_CSV.exists():
        print(f"[ERROR] Test dataset not found: {TEST_CSV}")
        print("Run create_100000_test_errors.py first to create the test dataset.")
        return None
    
    # Load test data
    df = pd.read_csv(TEST_CSV)
    print(f"\n[INFO] Loaded {len(df)} test samples")
    
    # Import detection function (suppress app.py startup prints)
    try:
        sys.path.insert(0, str(HERE))
        # Redirect stdout during import to suppress app.py startup messages
        with open(os.devnull, 'w', encoding='utf-8') as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                from app import detect_error_type_hybrid
        print("[INFO] Successfully imported detection functions")
    except ImportError as e:
        print(f"[ERROR] Could not import detect_error_type_hybrid: {e}")
        print("\n[INFO] Make sure you have activated the virtual environment:")
        print("   Windows: venv\\Scripts\\activate")
        print("   Linux/Mac: source venv/bin/activate")
        print("\n[INFO] Or install dependencies: pip install -r requirements.txt")
        traceback.print_exc()
        return None
    except Exception as e:
        print(f"[ERROR] Could not import detect_error_type_hybrid: {e}")
        traceback.print_exc()
        return None
    
    results = []
    correct = 0
    incorrect = 0
    error_type_stats = defaultdict(lambda: {'correct': 0, 'total': 0, 'incorrect': []})
    multi_error_correct = 0
    multi_error_total = 0
    
    print(f"\n[INFO] Testing error classification on {len(df)} examples...")
    print("This may take a while...\n")
    
    for idx, row in df.iterrows():
        issue = row['user_text']
        expected = row['error_type']
        expected_types = str(row.get('error_types', expected)).split(', ')
        
        try:
            result = detect_error_type_hybrid(issue)
            predicted = result.get('label', 'None')
            confidence = result.get('confidence', 0.0)
            source = result.get('source', 'unknown')
            alternatives = result.get('alternatives', [])
            
            # Check if correct (primary type matches)
            is_correct = predicted == expected
            
            # For multi-error types, check if any expected type is in predictions
            is_multi_correct = False
            if len(expected_types) > 1:
                multi_error_total += 1
                # Check if predicted type is in expected types
                if predicted in expected_types:
                    is_multi_correct = True
                    multi_error_correct += 1
                # Also check alternatives
                elif any(alt.get('label') in expected_types for alt in alternatives):
                    is_multi_correct = True
                    multi_error_correct += 1
            
            # Update stats
            error_type_stats[expected]['total'] += 1
            if is_correct:
                correct += 1
                error_type_stats[expected]['correct'] += 1
            else:
                incorrect += 1
                error_type_stats[expected]['incorrect'].append({
                    'issue': issue,
                    'expected': expected,
                    'expected_types': expected_types,
                    'predicted': predicted,
                    'confidence': confidence,
                    'alternatives': [alt.get('label') for alt in alternatives[:3]]
                })
            
            results.append({
                'issue': issue,
                'expected': expected,
                'expected_types': expected_types,
                'predicted': predicted,
                'confidence': confidence,
                'source': source,
                'correct': is_correct,
                'multi_error': len(expected_types) > 1,
                'multi_correct': is_multi_correct if len(expected_types) > 1 else None
            })
            
            # Progress indicator
            if (idx + 1) % 10000 == 0:
                print(f"  Processed {idx + 1}/{len(df)} examples...")
                print(f"    Current accuracy: {(correct / (idx + 1)) * 100:.2f}%")
                
        except Exception as e:
            print(f"[ERROR] Failed to process: {issue[:50]}... - {e}")
            incorrect += 1
            error_type_stats[expected]['total'] += 1
            results.append({
                'issue': issue,
                'expected': expected,
                'expected_types': expected_types,
                'predicted': None,
                'confidence': 0.0,
                'source': 'error',
                'correct': False,
                'multi_error': len(expected_types) > 1,
                'multi_correct': None
            })
    
    # Calculate overall accuracy
    total = len(results)
    accuracy = (correct / total) * 100 if total > 0 else 0
    multi_accuracy = (multi_error_correct / multi_error_total) * 100 if multi_error_total > 0 else 0
    
    print(f"\n{'='*80}")
    print(f"ERROR CLASSIFICATION RESULTS")
    print(f"{'='*80}")
    print(f"Total Tested: {total:,}")
    print(f"Correct: {correct:,}")
    print(f"Incorrect: {incorrect:,}")
    print(f"Overall Accuracy: {accuracy:.2f}%")
    print(f"\nMulti-Error Type Results:")
    print(f"  Total Multi-Error Cases: {multi_error_total:,}")
    print(f"  Correct (any type matched): {multi_error_correct:,}")
    print(f"  Multi-Error Accuracy: {multi_accuracy:.2f}%")
    
    # Per-error-type accuracy
    print(f"\n{'='*80}")
    print(f"PER-ERROR-TYPE ACCURACY (Top 20)")
    print(f"{'='*80}")
    print(f"{'Error Type':<30} {'Accuracy':<15} {'Correct/Total'}")
    print(f"{'-'*80}")
    
    type_accuracies = []
    for error_type, stats in sorted(error_type_stats.items()):
        if stats['total'] > 0:
            type_accuracy = (stats['correct'] / stats['total']) * 100
            type_accuracies.append((error_type, type_accuracy, stats['correct'], stats['total']))
    
    # Sort by accuracy
    type_accuracies.sort(key=lambda x: x[1])
    
    # Show worst and best
    print("\nWorst Performing (Bottom 10):")
    for error_type, acc, correct_count, total_count in type_accuracies[:10]:
        print(f"  {error_type:<30} {acc:>6.2f}%        {correct_count}/{total_count}")
    
    print("\nBest Performing (Top 10):")
    for error_type, acc, correct_count, total_count in type_accuracies[-10:][::-1]:
        print(f"  {error_type:<30} {acc:>6.2f}%        {correct_count}/{total_count}")
    
    # Collect incorrect predictions for retraining
    incorrect_rows = []
    for r in results:
        if not r['correct']:
            try:
                # Clean the data to ensure it's CSV-safe
                issue_text = str(r['issue']).replace('\n', ' ').replace('\r', ' ').strip()
                error_type = str(r['expected']).strip()
                
                incorrect_rows.append({
                    'user_text': issue_text,
                    'error_type': error_type,
                    'component_label': error_type,
                    'source': 'incorrect_prediction_correction'
                })
            except Exception as e:
                print(f"[WARNING] Skipping row due to error: {e}")
                continue
    
    incorrect_df = pd.DataFrame(incorrect_rows)
    
    if len(incorrect_df) > 0:
        incorrect_file = DATA_DIR / "incorrect_error_predictions_100000.csv"
        try:
            # Save in chunks if file is very large
            if len(incorrect_df) > 50000:
                print(f"[INFO] Large dataset ({len(incorrect_df):,} rows), saving in chunks...")
                incorrect_df.head(50000).to_csv(incorrect_file, index=False, encoding='utf-8', errors='replace')
                print(f"[INFO] Saved first 50,000 rows. Total incorrect: {len(incorrect_df):,}")
            else:
                incorrect_df.to_csv(incorrect_file, index=False, encoding='utf-8', errors='replace')
            
            print(f"\n{'='*80}")
            print(f"INCORRECT PREDICTIONS SAVED FOR RETRAINING")
            print(f"{'='*80}")
            print(f"File: {incorrect_file}")
            print(f"Count: {len(incorrect_df):,} incorrect predictions")
        except Exception as e:
            print(f"\n[ERROR] Failed to save incorrect predictions: {e}")
            print(f"[INFO] Attempting to save with error handling...")
            try:
                incorrect_df.to_csv(incorrect_file, index=False, encoding='utf-8', errors='replace', quoting=1)
                print(f"✅ Saved with error handling")
            except Exception as e2:
                print(f"[ERROR] Still failed: {e2}")
    
    return {
        'results': results,
        'accuracy': accuracy,
        'multi_accuracy': multi_accuracy,
        'incorrect_df': incorrect_df,
        'error_type_stats': error_type_stats
    }

def test_hardware_recommendation():
    """Test hardware recommendation accuracy."""
    print("\n\n" + "=" * 80)
    print("TESTING HARDWARE RECOMMENDATION")
    print("=" * 80)
    
    if not TEST_CSV.exists():
        print(f"[ERROR] Test dataset not found: {TEST_CSV}")
        return None
    
    # Load test data
    df = pd.read_csv(TEST_CSV)
    print(f"\n[INFO] Loaded {len(df)} test samples")
    
    # Import hardware recommendation function (suppress app.py startup prints)
    try:
        sys.path.insert(0, str(HERE))
        # Redirect stdout during import to suppress app.py startup messages
        with open(os.devnull, 'w', encoding='utf-8') as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                from app import product_need_recommend
                from app import ProductNeedRequest
        print("[INFO] Successfully imported hardware recommendation functions")
    except ImportError as e:
        print(f"[ERROR] Could not import hardware recommendation functions: {e}")
        print("\n[INFO] Make sure you have activated the virtual environment:")
        print("   Windows: venv\\Scripts\\activate")
        print("   Linux/Mac: source venv/bin/activate")
        print("\n[INFO] Or install dependencies: pip install -r requirements.txt")
        traceback.print_exc()
        return None
    except Exception as e:
        print(f"[ERROR] Could not import hardware recommendation functions: {e}")
        traceback.print_exc()
        return None
    
    results = []
    correct = 0
    incorrect = 0
    component_stats = defaultdict(lambda: {'correct': 0, 'total': 0, 'incorrect': []})
    
    print(f"\n[INFO] Testing hardware recommendation on {len(df)} examples...")
    print("This may take a while...\n")
    
    # Sample subset for hardware testing (since it's more complex)
    # Test on 10,000 samples for speed
    test_df = df.sample(n=min(10000, len(df)), random_state=42)
    
    for idx, row in test_df.iterrows():
        issue = row['user_text']
        expected_component = row.get('component_label', row['error_type'])
        
        try:
            # Call hardware recommendation
            req = ProductNeedRequest(text=issue, budget="medium", district="Colombo")
            response = product_need_recommend(req)
            
            predicted = response.component if hasattr(response, 'component') else None
            confidence = response.confidence if hasattr(response, 'confidence') else 0.0
            
            # Check if correct (exact match or related)
            is_correct = (predicted == expected_component) if predicted else False
            
            # Update stats
            component_stats[expected_component]['total'] += 1
            if is_correct:
                correct += 1
                component_stats[expected_component]['correct'] += 1
            else:
                incorrect += 1
                component_stats[expected_component]['incorrect'].append({
                    'issue': issue,
                    'expected': expected_component,
                    'predicted': predicted,
                    'confidence': confidence
                })
            
            results.append({
                'issue': issue,
                'expected': expected_component,
                'predicted': predicted,
                'confidence': confidence,
                'correct': is_correct
            })
            
            # Progress indicator
            if (idx + 1) % 1000 == 0:
                print(f"  Processed {idx + 1}/{len(test_df)} examples...")
                print(f"    Current accuracy: {(correct / (idx + 1)) * 100:.2f}%")
                
        except Exception as e:
            print(f"[ERROR] Failed to process: {issue[:50]}... - {e}")
            incorrect += 1
            component_stats[expected_component]['total'] += 1
            results.append({
                'issue': issue,
                'expected': expected_component,
                'predicted': None,
                'confidence': 0.0,
                'correct': False
            })
    
    # Calculate overall accuracy
    total = len(results)
    accuracy = (correct / total) * 100 if total > 0 else 0
    
    print(f"\n{'='*80}")
    print(f"HARDWARE RECOMMENDATION RESULTS")
    print(f"{'='*80}")
    print(f"Total Tested: {total:,}")
    print(f"Correct: {correct:,}")
    print(f"Incorrect: {incorrect:,}")
    print(f"Overall Accuracy: {accuracy:.2f}%")
    
    # Collect incorrect predictions for retraining
    incorrect_rows = []
    for r in results:
        if not r['correct']:
            try:
                # Clean the data to ensure it's CSV-safe
                issue_text = str(r['issue']).replace('\n', ' ').replace('\r', ' ').strip()
                component_label = str(r['expected']).strip()
                
                incorrect_rows.append({
                    'user_text': issue_text,
                    'component_label': component_label,
                    'source': 'incorrect_hardware_prediction_correction'
                })
            except Exception as e:
                print(f"[WARNING] Skipping row due to error: {e}")
                continue
    
    incorrect_df = pd.DataFrame(incorrect_rows)
    
    if len(incorrect_df) > 0:
        incorrect_file = DATA_DIR / "incorrect_hardware_predictions_100000.csv"
        try:
            incorrect_df.to_csv(incorrect_file, index=False, encoding='utf-8', errors='replace')
            print(f"\n{'='*80}")
            print(f"INCORRECT HARDWARE PREDICTIONS SAVED FOR RETRAINING")
            print(f"{'='*80}")
            print(f"File: {incorrect_file}")
            print(f"Count: {len(incorrect_df):,} incorrect predictions")
        except Exception as e:
            print(f"\n[ERROR] Failed to save incorrect hardware predictions: {e}")
            try:
                incorrect_df.to_csv(incorrect_file, index=False, encoding='utf-8', errors='replace', quoting=1)
                print(f"✅ Saved with error handling")
            except Exception as e2:
                print(f"[ERROR] Still failed: {e2}")
    
    return {
        'results': results,
        'accuracy': accuracy,
        'incorrect_df': incorrect_df,
        'component_stats': component_stats
    }

def main():
    """Run comprehensive tests."""
    print("=" * 80)
    print("COMPREHENSIVE TEST: 100,000 PC ERRORS")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test error classification
    error_results = test_error_classification()
    
    # Test hardware recommendation
    hardware_results = test_hardware_recommendation()
    
    # Save summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'error_classification': {
            'accuracy': error_results['accuracy'] if error_results else None,
            'multi_accuracy': error_results['multi_accuracy'] if error_results else None,
            'incorrect_count': len(error_results['incorrect_df']) if error_results else 0
        },
        'hardware_recommendation': {
            'accuracy': hardware_results['accuracy'] if hardware_results else None,
            'incorrect_count': len(hardware_results['incorrect_df']) if hardware_results else 0
        }
    }
    
    summary_file = HERE / "test_100000_results_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"TEST SUMMARY SAVED")
    print(f"{'='*80}")
    print(f"File: {summary_file}")
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()

