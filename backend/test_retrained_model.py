"""
Test the retrained error detection model directly.
"""

import joblib
from pathlib import Path
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
MODEL_PATH = HERE / "nlp_error_model_error_type.pkl"

# Test cases - including new issues from solutions
TEST_CASES = [
    ("My PC not turning on", "PSU / Power Issue"),
    ("PC very slow", "Slow Performance"),
    ("RAM not detected", "RAM Upgrade"),
    ("PC slow opening files", "SSD Upgrade"),
    ("No internet on PC", "Wi-Fi Adapter Upgrade"),
    ("Screen black PC on", "No Display / No Signal"),
    ("PC very hot", "CPU Overheat"),
    ("PC blue screen", "Blue Screen (BSOD)"),
    ("PC not boot", "Windows Boot Failure"),
    ("My PC not working properly", "General Repair"),
    # New test cases from solutions
    ("PC not turning on", "PSU / Power Issue"),
    ("No power at all", "PSU / Power Issue"),
    ("Power button not working", "PSU / Power Issue"),
    ("PC start then off", "PSU / Power Issue"),
    ("PC restart again and again", "RAM Upgrade"),
    ("PC stuck black screen", "No Display / No Signal"),
    ("Fan spin no display", "No Display / No Signal"),
    ("PC stuck on logo", "Windows Boot Failure"),
    ("PC beep sound", "RAM Upgrade"),
    ("PC start slow then freeze", "SSD Upgrade"),
    ("PC off suddenly", "CPU Overheat"),
    ("PC lag always", "Slow Performance"),
    ("Laptop slow boot", "SSD Upgrade"),
    ("PC freeze often", "RAM Upgrade"),
    ("PC slow after update", "Slow Performance"),
    ("PC lag typing", "Slow Performance"),
    ("PC slow browsing", "Slow Performance"),
    ("PC hang multitask", "RAM Upgrade"),
    ("PC slow file open", "SSD Upgrade"),
    ("PC slow gaming", "GPU Upgrade"),
]


def test_model():
    """Test the model directly."""
    print("=" * 80)
    print("TESTING RETRAINED ERROR DETECTION MODEL")
    print("=" * 80)
    
    if not MODEL_PATH.exists():
        print(f"[ERROR] Model not found: {MODEL_PATH}")
        return
    
    try:
        model = joblib.load(MODEL_PATH)
        print(f"[INFO] Model loaded successfully\n")
        
        correct = 0
        total = len(TEST_CASES)
        
        for issue, expected in TEST_CASES:
            # Predict
            prediction = model.predict([issue.lower()])[0]
            probabilities = model.predict_proba([issue.lower()])[0]
            classes = model.classes_
            
            # Get confidence
            pred_idx = list(classes).index(prediction)
            confidence = probabilities[pred_idx]
            
            is_correct = prediction == expected
            if is_correct:
                correct += 1
                status = "[OK]"
            else:
                status = "[X]"
            
            print(f"{status} '{issue}'")
            print(f"    Expected: {expected}")
            print(f"    Predicted: {prediction} (confidence: {confidence:.2f})")
            print()
        
        accuracy = (correct / total) * 100
        print(f"{'='*80}")
        print(f"Results: {correct}/{total} correct ({accuracy:.1f}%)")
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"[ERROR] Failed to test model: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_model()

