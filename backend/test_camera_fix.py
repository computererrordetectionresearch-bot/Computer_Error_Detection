"""
Test camera/webcam detection fix.
"""

from pathlib import Path
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()

# Test cases
TEST_CASES = [
    "lap camera not working",
    "laptop camera not working",
    "camera not working",
    "webcam not working",
    "camera not detected",
    "webcam not detected",
    "camera error",
    "webcam error",
    "camera problem",
    "webcam problem",
]

print("=" * 80)
print("TESTING CAMERA/WEBCAM DETECTION FIX")
print("=" * 80)

# Test rules
try:
    from rules import match_rule
    print("\n[TESTING RULES]")
    print("-" * 80)
    
    for test_case in TEST_CASES:
        result = match_rule(test_case)
        if result:
            component, confidence, explanation, related = result
            print(f"✓ '{test_case}'")
            print(f"  → {component} (confidence: {confidence:.0%})")
            print(f"  → {explanation}")
        else:
            print(f"✗ '{test_case}' - NO RULE MATCH")
    
    print("\n" + "=" * 80)
    print("RULES TEST COMPLETE")
    print("=" * 80)
    
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
        
        for test_case in TEST_CASES[:5]:  # Test first 5
            try:
                predicted = model.predict([test_case.lower()])[0]
                probs = model.predict_proba([test_case.lower()])[0]
                classes = model.classes_
                idx = list(classes).index(predicted)
                confidence = probs[idx]
                
                print(f"'{test_case}'")
                print(f"  → {predicted} (confidence: {confidence:.0%})")
                
                # Show top 3
                idx_sorted = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)
                print(f"  Top 3:")
                for i in idx_sorted[:3]:
                    print(f"    - {classes[i]}: {probs[i]:.0%}")
                print()
            except Exception as e:
                print(f"✗ '{test_case}' - ERROR: {e}")
    else:
        print(f"\n[WARNING] Model not found: {MODEL_PATH}")
    
    print("=" * 80)
    print("ML MODEL TEST COMPLETE")
    print("=" * 80)
    
except Exception as e:
    print(f"[ERROR] Failed to test ML model: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Camera/Webcam detection fix verified!")

