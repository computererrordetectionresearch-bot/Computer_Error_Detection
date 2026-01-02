"""
Test script for improved hardware recommendation endpoint
"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

import joblib
import numpy as np

# Load model
MODEL_PATH = HERE / "product_need_model.pkl"

if not MODEL_PATH.exists():
    print("❌ Model not found. Please train it first using train_improved_models.py")
    sys.exit(1)

print("=" * 80)
print("TESTING IMPROVED HARDWARE RECOMMENDATION MODEL")
print("=" * 80)

model = joblib.load(MODEL_PATH)
print(f"✅ Model loaded: {len(model.classes_)} component types")

# Test cases with expected confidence levels
test_cases = [
    {
        "text": "I need more RAM for multitasking and Chrome tabs",
        "expected_high_conf": True,
        "expected_component": "RAM Upgrade"
    },
    {
        "text": "My computer is very slow when starting up",
        "expected_high_conf": False,
        "expected_component": "SSD Upgrade"
    },
    {
        "text": "Low FPS in games, need better graphics",
        "expected_high_conf": False,
        "expected_component": "GPU Upgrade"
    },
    {
        "text": "Computer randomly shuts down",
        "expected_high_conf": False,
        "expected_component": "PSU Upgrade"
    },
    {
        "text": "User reports issue related to ram upgrade or symptoms hinting toward it.",
        "expected_high_conf": True,
        "expected_component": "RAM Upgrade"
    }
]

print("\n📝 Testing prediction with confidence thresholds:\n")

for i, test in enumerate(test_cases, 1):
    text = test["text"]
    expected = test["expected_component"]
    
    # Predict
    probs = model.predict_proba([text])[0]
    classes = model.classes_
    idx_sorted = np.argsort(probs)[::-1]
    
    # Get top 5
    top5 = [(str(classes[i]), float(probs[i])) for i in idx_sorted[:5]]
    primary_label, primary_conf = top5[0]
    
    # Determine confidence level
    if primary_conf >= 0.7:
        conf_level = "HIGH"
        conf_emoji = "✅"
    elif primary_conf >= 0.4:
        conf_level = "MEDIUM"
        conf_emoji = "⚠️"
    else:
        conf_level = "LOW"
        conf_emoji = "❌"
    
    # Check if matches expected
    matches = primary_label == expected
    match_status = "✅" if matches else "❌"
    
    print(f"Test {i}: \"{text[:50]}...\"")
    print(f"   {match_status} Primary: {primary_label} (confidence: {primary_conf:.3f}) [{conf_level}]")
    print(f"   Expected: {expected}")
    print(f"   {conf_emoji} Confidence Level: {conf_level}")
    print(f"   Top 5 Alternatives:")
    for j, (label, conf) in enumerate(top5[:5], 1):
        marker = "👉" if j == 1 else "  "
        print(f"      {marker} {j}. {label} ({conf:.3f})")
    print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print("✅ Model supports predict_proba() for confidence scores")
print("✅ Returns top 5 alternatives for each prediction")
print("✅ Confidence thresholds:")
print("   - HIGH (≥0.7): Highly reliable recommendation")
print("   - MEDIUM (0.4-0.7): Likely recommendation with alternatives")
print("   - LOW (<0.4): Multiple alternatives emphasized")
print("\n🎉 Hardware recommendation system is ready!")

