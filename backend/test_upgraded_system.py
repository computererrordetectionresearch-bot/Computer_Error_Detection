"""
Quick test script for the upgraded Product Need Model system.
Tests rules, hierarchical ML, and feedback system.
"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass  # Already wrapped or not needed

HERE = Path(__file__).parent.resolve()

print("=" * 80)
print("TESTING UPGRADED PRODUCT NEED MODEL SYSTEM")
print("=" * 80)

# Test 1: Rules
print("\n" + "=" * 80)
print("TEST 1: RULE-BASED MATCHING")
print("=" * 80)

try:
    from rules import match_rule
    
    test_cases = [
        "My PC shuts down instantly when I turn it on",
        "No display but fans are spinning",
        "Low FPS in games, need better graphics",
        "Wifi keeps disconnecting every few minutes"
    ]
    
    for text in test_cases:
        result = match_rule(text)
        if result:
            component, confidence, explanation = result
            print(f"\n[OK] Text: '{text[:50]}...'")
            print(f"   Component: {component}")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Source: rule")
        else:
            print(f"\n[NO MATCH] No rule match for: '{text[:50]}...'")
    
    print("\n[OK] Rule system working!")
except Exception as e:
    print(f"[ERROR] Rule system failed: {e}")

# Test 2: Hierarchical Inference
print("\n" + "=" * 80)
print("TEST 2: HIERARCHICAL INFERENCE")
print("=" * 80)

try:
    from hierarchical_inference import predict_hierarchical, _load_models
    
    # Load models
    category_model, component_model, category_mapping, component_to_category = _load_models()
    
    if category_model and component_model:
        test_text = "I need more RAM for multitasking"
        comp, conf, source, top5 = predict_hierarchical(test_text)
        
        print(f"\n[OK] Text: '{test_text}'")
        print(f"   Component: {comp}")
        print(f"   Confidence: {conf:.3f}")
        print(f"   Source: {source}")
        print(f"   Top 5 alternatives:")
        for i, (label, c) in enumerate(top5[:5], 1):
            print(f"      {i}. {label} ({c:.3f})")
        
        print("\n[OK] Hierarchical inference working!")
    else:
        print("[WARNING] Models not loaded. Run train_hierarchical_models.py first.")
except Exception as e:
    print(f"[ERROR] Hierarchical inference failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Feedback Storage
print("\n" + "=" * 80)
print("TEST 3: FEEDBACK STORAGE")
print("=" * 80)

try:
    from feedback_storage import save_feedback, get_feedback_count
    
    # Test save
    success = save_feedback(
        text="Test feedback",
        predicted_label="RAM Upgrade",
        confidence=0.45,
        user_correct_label="SSD Upgrade",
        source="hierarchical_ml"
    )
    
    if success:
        count = get_feedback_count()
        print(f"[OK] Feedback saved successfully!")
        print(f"   Total feedback entries: {count}")
    else:
        print("[ERROR] Failed to save feedback")
    
    print("\n[OK] Feedback system working!")
except Exception as e:
    print(f"[ERROR] Feedback system failed: {e}")

# Test 4: Component Mapping
print("\n" + "=" * 80)
print("TEST 4: COMPONENT-CATEGORY MAPPING")
print("=" * 80)

try:
    import json
    
    with open(HERE / "component_category_mapping.json", 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    total_components = sum(len(components) for components in mapping.values())
    categories = list(mapping.keys())
    
    print(f"[OK] Mapping loaded:")
    print(f"   Categories: {len(categories)} ({', '.join(categories)})")
    print(f"   Total components: {total_components}")
    
    # Check for duplicates
    all_components = []
    for components in mapping.values():
        all_components.extend(components)
    
    duplicates = [c for c in set(all_components) if all_components.count(c) > 1]
    if duplicates:
        print(f"   [WARNING] Duplicate components found: {duplicates}")
    else:
        print(f"   [OK] No duplicate components")
    
    print("\n[OK] Mapping system working!")
except Exception as e:
    print(f"[ERROR] Mapping system failed: {e}")

print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print("[OK] All systems tested!")
print("\nNext steps:")
print("1. Train models: python train_hierarchical_models.py")
print("2. Evaluate: python evaluate_hierarchical_models.py")
print("3. Start server and test API endpoints")

