"""
Test the error detection model directly on 1000 error examples.
Loads model directly without importing app.py.
"""

from pathlib import Path
import pandas as pd
import joblib
import sys
import io
import json
from collections import defaultdict
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()
TEST_CSV = DATA_DIR / "test_1000_errors.csv"
MODEL_PATH = HERE / "nlp_error_model_error_type.pkl"


def rule_based_detection(text: str) -> tuple:
    """Simple rule-based detection (from app.py logic)."""
    text_lower = text.lower().strip()
    
    # Power issues
    if any(kw in text_lower for kw in ["not turning on", "no power", "power button", "dead", "power cut", "start then off", "restart again", "shutdown suddenly", "charging", "power flicker", "power noise", "power delay", "auto shutdown", "no power LED", "power click", "not start cold", "no power sometimes"]):
        return "PSU / Power Issue", 0.85
    
    # Boot issues
    if any(kw in text_lower for kw in ["not boot", "boot failure", "boot loop", "stuck on logo", "stuck loading", "stuck booting", "boot fail", "no boot device", "stuck repair", "stuck restart", "boot error", "boot only BIOS"]):
        return "Windows Boot Failure", 0.85
    
    # Display issues
    if any(kw in text_lower for kw in ["no display", "black screen", "no signal", "blank screen", "fan spin but no display", "light on but screen black", "on then blank", "no display HDMI", "no display VGA", "no signal display", "no display but on"]):
        return "No Display / No Signal", 0.85
    
    # Overheating
    if any(kw in text_lower for kw in ["overheat", "too hot", "temperature high", "thermal", "heating", "hot", "fan", "cooling"]):
        if any(kw in text_lower for kw in ["game", "gaming", "gpu", "graphics"]):
            return "GPU Overheat", 0.85
        else:
            return "CPU Overheat", 0.85
    
    # BSOD
    if any(kw in text_lower for kw in ["blue screen", "bsod", "stop code", "crash suddenly"]):
        return "Blue Screen (BSOD)", 0.85
    
    # Slow performance
    if any(kw in text_lower for kw in ["slow", "lag", "freeze", "hang", "stutter", "delay", "unresponsive", "sluggish"]):
        if any(kw in text_lower for kw in ["boot", "startup", "loading", "opening files", "file open", "copy files"]):
            return "SSD Upgrade", 0.75
        elif any(kw in text_lower for kw in ["multitask", "ram", "memory"]):
            return "RAM Upgrade", 0.75
        elif any(kw in text_lower for kw in ["gaming", "game", "gpu", "graphics"]):
            return "GPU Upgrade", 0.75
        else:
            return "Slow Performance", 0.75
    
    # RAM issues
    if any(kw in text_lower for kw in ["ram", "memory", "beep sound"]):
        return "RAM Upgrade", 0.85
    
    # Storage issues
    if any(kw in text_lower for kw in ["ssd", "hdd", "storage", "disk", "hard drive"]):
        return "SSD Upgrade", 0.75
    
    # Network issues
    if any(kw in text_lower for kw in ["internet", "wifi", "wi-fi", "network", "ethernet"]):
        return "Wi-Fi Adapter Upgrade", 0.75
    
    # Driver issues
    if any(kw in text_lower for kw in ["driver", "drivers"]):
        return "Driver Issue", 0.75
    
    # General
    return "General Repair", 0.5


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
    
    # Load ML model if available
    ml_model = None
    if MODEL_PATH.exists():
        try:
            ml_model = joblib.load(MODEL_PATH)
            print(f"[INFO] ML model loaded: {MODEL_PATH}")
        except Exception as e:
            print(f"[WARNING] Could not load ML model: {e}")
    
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
            # Try rule-based first
            rule_pred, rule_conf = rule_based_detection(issue)
            
            # Try ML model if available
            ml_pred = None
            ml_conf = 0.0
            if ml_model:
                try:
                    ml_pred = ml_model.predict([issue.lower()])[0]
                    ml_probs = ml_model.predict_proba([issue.lower()])[0]
                    ml_classes = ml_model.classes_
                    ml_idx = list(ml_classes).index(ml_pred)
                    ml_conf = ml_probs[ml_idx]
                except:
                    pass
            
            # Choose prediction (rule if high confidence, else ML)
            if rule_conf >= 0.8:
                predicted = rule_pred
                confidence = rule_conf
                source = "rule"
            elif ml_pred and ml_conf > rule_conf:
                predicted = ml_pred
                confidence = ml_conf
                source = "ml"
            else:
                predicted = rule_pred
                confidence = rule_conf
                source = "rule"
            
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
                print(f"  Processed {idx + 1}/{len(df)} examples... (Accuracy so far: {correct/(idx+1)*100:.1f}%)")
                
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
    
    # Show worst 10
    print("\nWorst 10:")
    for error_type, acc, correct, total in type_accuracies[:10]:
        print(f"{error_type:<30} {acc:>6.2f}%        {correct}/{total}")
    
    # Show best 10
    print("\nBest 10:")
    for error_type, acc, correct, total in type_accuracies[-10:]:
        print(f"{error_type:<30} {acc:>6.2f}%        {correct}/{total}")
    
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
    
    # Save summary
    results_file = HERE / "test_1000_results_summary.json"
    summary = {
        'overall': {
            'total': total,
            'correct': correct,
            'incorrect': incorrect,
            'accuracy': accuracy
        },
        'per_type': {
            k: {
                'correct': v['correct'],
                'total': v['total'],
                'accuracy': (v['correct'] / v['total'] * 100) if v['total'] > 0 else 0
            }
            for k, v in error_type_stats.items()
        }
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"Summary saved to: {results_file}")
    print(f"{'='*80}")
    
    return results, accuracy, incorrect_df


if __name__ == "__main__":
    test_model()

