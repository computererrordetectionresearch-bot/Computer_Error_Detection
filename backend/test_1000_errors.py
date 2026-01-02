"""
Test the error detection model on 1000 different error examples.
Analyze accuracy and identify incorrect predictions for retraining.
"""

from pathlib import Path
import pandas as pd
import sys
import io
import json
from collections import defaultdict

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()
TEST_CSV = DATA_DIR / "test_1000_errors.csv"


def test_model():
    """Test the model on 1000 error examples."""
    print("=" * 80)
    print("TESTING MODEL ON 1000 ERROR EXAMPLES")
    print("=" * 80)
    
    if not TEST_CSV.exists():
        print(f"[ERROR] Test dataset not found: {TEST_CSV}")
        print("Run create_1000_test_errors.py first to create the test dataset.")
        return
    
    # Load test data
    df = pd.read_csv(TEST_CSV)
    print(f"\n[INFO] Loaded {len(df)} test samples")
    
    # Import detection function
    try:
        sys.path.insert(0, str(HERE))
        from app import detect_error_type_hybrid
    except Exception as e:
        print(f"[ERROR] Could not import detect_error_type_hybrid: {e}")
        return
    
    results = []
    correct = 0
    incorrect = 0
    error_type_stats = defaultdict(lambda: {'correct': 0, 'total': 0, 'incorrect': []})
    
    print(f"\n[INFO] Testing model on {len(df)} examples...")
    print("This may take a few minutes...\n")
    
    for idx, row in df.iterrows():
        issue = row['user_text']
        expected = row['error_type']
        
        try:
            result = detect_error_type_hybrid(issue)
            predicted = result.get('label', 'None')
            confidence = result.get('confidence', 0.0)
            source = result.get('source', 'unknown')
            
            is_correct = predicted == expected
            
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
                    'predicted': predicted,
                    'confidence': confidence
                })
            
            results.append({
                'issue': issue,
                'expected': expected,
                'predicted': predicted,
                'confidence': confidence,
                'source': source,
                'correct': is_correct
            })
            
            # Progress indicator
            if (idx + 1) % 100 == 0:
                print(f"  Processed {idx + 1}/{len(df)} examples...")
                
        except Exception as e:
            print(f"[ERROR] Failed to process: {issue} - {e}")
            incorrect += 1
            error_type_stats[expected]['total'] += 1
            results.append({
                'issue': issue,
                'expected': expected,
                'predicted': None,
                'confidence': 0.0,
                'source': 'error',
                'correct': False
            })
    
    # Calculate overall accuracy
    total = len(results)
    accuracy = (correct / total) * 100 if total > 0 else 0
    
    print(f"\n{'='*80}")
    print(f"OVERALL RESULTS")
    print(f"{'='*80}")
    print(f"Total Tested: {total}")
    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(f"Accuracy: {accuracy:.2f}%")
    
    # Per-error-type accuracy
    print(f"\n{'='*80}")
    print(f"PER-ERROR-TYPE ACCURACY")
    print(f"{'='*80}")
    print(f"{'Error Type':<30} {'Accuracy':<15} {'Correct/Total'}")
    print(f"{'-'*80}")
    
    type_accuracies = []
    for error_type, stats in sorted(error_type_stats.items()):
        if stats['total'] > 0:
            type_accuracy = (stats['correct'] / stats['total']) * 100
            type_accuracies.append((error_type, type_accuracy, stats['correct'], stats['total']))
            print(f"{error_type:<30} {type_accuracy:>6.2f}%        {stats['correct']}/{stats['total']}")
    
    # Find worst performing error types
    type_accuracies.sort(key=lambda x: x[1])
    worst_types = type_accuracies[:10]
    
    print(f"\n{'='*80}")
    print(f"WORST PERFORMING ERROR TYPES (Top 10)")
    print(f"{'='*80}")
    for error_type, acc, correct, total in worst_types:
        print(f"{error_type:<30} {acc:>6.2f}% ({correct}/{total})")
    
    # Collect incorrect predictions for retraining
    incorrect_df = pd.DataFrame([
        {
            'user_text': r['issue'],
            'error_type': r['expected'],
            'component_label': r['expected'],
            'source': 'incorrect_prediction_correction'
        }
        for r in results if not r['correct']
    ])
    
    if len(incorrect_df) > 0:
        incorrect_file = DATA_DIR / "incorrect_predictions_for_retraining.csv"
        incorrect_df.to_csv(incorrect_file, index=False, encoding='utf-8')
        print(f"\n{'='*80}")
        print(f"INCORRECT PREDICTIONS SAVED FOR RETRAINING")
        print(f"{'='*80}")
        print(f"File: {incorrect_file}")
        print(f"Count: {len(incorrect_df)} incorrect predictions")
        print(f"\nThese will be used to retrain the model.")
    
    # Save full results
    results_file = HERE / "test_1000_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total': total,
                'correct': correct,
                'incorrect': incorrect,
                'accuracy': accuracy
            },
            'per_type_stats': {
                k: {
                    'correct': v['correct'],
                    'total': v['total'],
                    'accuracy': (v['correct'] / v['total'] * 100) if v['total'] > 0 else 0
                }
                for k, v in error_type_stats.items()
            },
            'results': results[:100]  # Save first 100 for review
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"Full results saved to: {results_file}")
    print(f"{'='*80}")
    
    return results, accuracy, incorrect_df


if __name__ == "__main__":
    test_model()

