"""
Test Zoom and other application-specific scenarios.
"""

from pathlib import Path
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()

# Test cases - application-specific scenarios
TEST_CASES = [
    ("zoom application not show my video", "Webcam Upgrade"),
    ("zoom not showing my video", "Webcam Upgrade"),
    ("zoom camera not working", "Webcam Upgrade"),
    ("can't see myself in zoom", "Webcam Upgrade"),
    ("teams camera not working", "Webcam Upgrade"),
    ("video call camera not working", "Webcam Upgrade"),
    ("chrome tabs closing automatically", "RAM Upgrade"),
    ("photoshop slow", "RAM Upgrade"),
    ("games take long to load", "SSD Upgrade"),
    ("valorant low fps", "GPU Upgrade"),
    ("netflix buffering", "WiFi Adapter Upgrade"),
    ("zoom no sound", "Audio Issue"),
    ("discord mic not working", "Microphone Upgrade"),
]

print("=" * 80)
print("TESTING APPLICATION-SPECIFIC SCENARIOS")
print("=" * 80)

# Test rules
try:
    from rules import match_rule
    print("\n[TESTING RULES]")
    print("-" * 80)
    
    correct = 0
    total = len(TEST_CASES)
    
    for text, expected in TEST_CASES:
        result = match_rule(text)
        if result:
            component, confidence, explanation, related = result
            is_correct = component == expected
            status = "✓" if is_correct else "✗"
            print(f"{status} '{text}'")
            print(f"    Expected: {expected}")
            print(f"    Got: {component} (confidence: {confidence:.0%})")
            if is_correct:
                correct += 1
        else:
            print(f"✗ '{text}' - NO RULE MATCH")
            print(f"    Expected: {expected}")
    
    print(f"\n{'='*80}")
    print(f"Rules Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    print(f"{'='*80}")
    
except Exception as e:
    print(f"[ERROR] Failed to test rules: {e}")
    import traceback
    traceback.print_exc()

# Test ML model
try:
    import joblib
    MODEL_PATH = HERE / "product_need_model.pkl"
    
    if MODEL_PATH.exists():
        print("\n[TESTING ML MODEL]")
        print("-" * 80)
        
        model = joblib.load(MODEL_PATH)
        
        correct = 0
        total = len(TEST_CASES)
        
        for text, expected in TEST_CASES:
            try:
                predicted = model.predict([text.lower()])[0]
                probs = model.predict_proba([text.lower()])[0]
                classes = model.classes_
                idx = list(classes).index(predicted)
                confidence = probs[idx]
                
                is_correct = predicted == expected
                status = "✓" if is_correct else "✗"
                print(f"{status} '{text}'")
                print(f"    Expected: {expected}")
                print(f"    Got: {predicted} (confidence: {confidence:.0%})")
                if is_correct:
                    correct += 1
                print()
            except Exception as e:
                print(f"✗ '{text}' - ERROR: {e}")
        
        print(f"{'='*80}")
        print(f"ML Model Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
        print(f"{'='*80}")
    else:
        print(f"\n[WARNING] Model not found: {MODEL_PATH}")
        print("Run: python train_improved_models.py")
    
except Exception as e:
    print(f"[ERROR] Failed to test ML model: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Application-specific scenario testing complete!")

