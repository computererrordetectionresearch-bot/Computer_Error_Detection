"""
Evaluate Product Need Model on broken English and real-world inputs.
Tests robustness with typos, short phrases, and informal language.
"""

from pathlib import Path
import pandas as pd
import sys
import io
import numpy as np
from typing import List, Tuple, Dict

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()

# Test cases with broken English
BROKEN_ENGLISH_TEST_CASES = [
    {
        "text": "my ps not start",
        "expected": ["PSU Upgrade", "Power Cable Replacement"],
        "category": "Power"
    },
    {
        "text": "pc vey slow",
        "expected": ["RAM Upgrade", "SSD Upgrade"],
        "category": "Performance"
    },
    {
        "text": "no internet in my pc",
        "expected": ["WiFi Adapter Upgrade", "Router Upgrade"],
        "category": "Network"
    },
    {
        "text": "my computer takes long time to boot and freezes",
        "expected": ["SSD Upgrade", "RAM Upgrade"],
        "category": "Performance"
    },
    {
        "text": "pc hot",
        "expected": ["CPU Cooler Upgrade", "Case Fan Upgrade"],
        "category": "Performance"
    },
    {
        "text": "no display",
        "expected": ["Monitor or GPU Check", "Display Cable Replacement"],
        "category": "Display"
    },
    {
        "text": "low fps games",
        "expected": ["GPU Upgrade", "RAM Upgrade"],
        "category": "Performance"
    },
    {
        "text": "wifi disconect",
        "expected": ["WiFi Adapter Upgrade"],
        "category": "Network"
    },
    {
        "text": "ram full",
        "expected": ["RAM Upgrade"],
        "category": "Performance"
    },
    {
        "text": "boot slow",
        "expected": ["SSD Upgrade"],
        "category": "Storage"
    }
]


def evaluate_with_hierarchical(text: str) -> Tuple[str, float, List[Tuple[str, float]]]:
    """Evaluate using hierarchical model."""
    try:
        from hierarchical_inference import predict_hierarchical
        comp, conf, source, top5, grouped = predict_hierarchical(text, return_multiple=True)
        return comp, conf, top5
    except Exception as e:
        print(f"[ERROR] Hierarchical evaluation failed: {e}")
        return None, 0.0, []


def evaluate_with_rules(text: str) -> Tuple[str, float, str]:
    """Evaluate using rules."""
    try:
        from rules import match_rule
        result = match_rule(text)
        if result:
            return result[0], result[1], result[2]
        return None, 0.0, ""
    except Exception as e:
        print(f"[ERROR] Rule evaluation failed: {e}")
        return None, 0.0, ""


def calculate_top_k_accuracy(predicted_list: List[str], expected_list: List[str], k: int = 3) -> bool:
    """Check if any expected component is in top-k predictions."""
    predicted_set = set(predicted_list[:k])
    expected_set = set(expected_list)
    return len(predicted_set.intersection(expected_set)) > 0


def main():
    """Main evaluation function."""
    print("=" * 80)
    print("BROKEN ENGLISH EVALUATION")
    print("=" * 80)
    
    results = []
    
    for i, test_case in enumerate(BROKEN_ENGLISH_TEST_CASES, 1):
        text = test_case["text"]
        expected = test_case["expected"]
        category = test_case["category"]
        
        print(f"\n{'='*80}")
        print(f"Test {i}: '{text}'")
        print(f"Expected: {', '.join(expected)}")
        print(f"Category: {category}")
        print(f"{'='*80}")
        
        # Test rules first
        rule_comp, rule_conf, rule_expl = evaluate_with_rules(text)
        if rule_comp:
            print(f"\n[RULE] Component: {rule_comp} (confidence: {rule_conf:.3f})")
            print(f"       Explanation: {rule_expl}")
            rule_correct = rule_comp in expected
            print(f"       {'✅ CORRECT' if rule_correct else '❌ INCORRECT'}")
        else:
            print(f"\n[RULE] No rule match")
            rule_correct = False
        
        # Test hierarchical ML
        ml_comp, ml_conf, ml_top5 = evaluate_with_hierarchical(text)
        if ml_comp:
            ml_predicted_list = [ml_comp] + [comp for comp, _ in ml_top5]
            print(f"\n[ML] Primary: {ml_comp} (confidence: {ml_conf:.3f})")
            print(f"     Top 5: {', '.join([f'{c}({conf:.2f})' for c, conf in ml_top5[:5]])}")
            
            # Check top-1 accuracy
            ml_top1_correct = ml_comp in expected
            # Check top-3 accuracy
            ml_top3_correct = calculate_top_k_accuracy(ml_predicted_list, expected, k=3)
            
            print(f"     Top-1: {'✅ CORRECT' if ml_top1_correct else '❌ INCORRECT'}")
            print(f"     Top-3: {'✅ CORRECT' if ml_top3_correct else '❌ INCORRECT'}")
        else:
            print(f"\n[ML] No prediction")
            ml_top1_correct = False
            ml_top3_correct = False
            ml_predicted_list = []
        
        results.append({
            "text": text,
            "expected": expected,
            "category": category,
            "rule_component": rule_comp,
            "rule_confidence": rule_conf,
            "rule_correct": rule_correct,
            "ml_component": ml_comp,
            "ml_confidence": ml_conf,
            "ml_top1_correct": ml_top1_correct,
            "ml_top3_correct": ml_top3_correct,
            "ml_top5": ml_predicted_list[:5]
        })
    
    # Summary
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    
    rule_correct_count = sum(1 for r in results if r["rule_correct"])
    ml_top1_correct_count = sum(1 for r in results if r["ml_top1_correct"])
    ml_top3_correct_count = sum(1 for r in results if r["ml_top3_correct"])
    
    total = len(results)
    
    print(f"\nRule-based:")
    print(f"  Accuracy: {rule_correct_count}/{total} ({rule_correct_count/total*100:.1f}%)")
    
    print(f"\nHierarchical ML:")
    print(f"  Top-1 Accuracy: {ml_top1_correct_count}/{total} ({ml_top1_correct_count/total*100:.1f}%)")
    print(f"  Top-3 Accuracy: {ml_top3_correct_count}/{total} ({ml_top3_correct_count/total*100:.1f}%)")
    
    # Confidence vs Coverage
    print(f"\nConfidence Analysis:")
    confidences = [r["ml_confidence"] for r in results if r["ml_confidence"] > 0]
    if confidences:
        print(f"  Average confidence: {np.mean(confidences):.3f}")
        print(f"  Min confidence: {np.min(confidences):.3f}")
        print(f"  Max confidence: {np.max(confidences):.3f}")
        
        # Coverage at different thresholds
        thresholds = [0.3, 0.5, 0.7, 0.9]
        for threshold in thresholds:
            covered = sum(1 for c in confidences if c >= threshold)
            correct_at_threshold = sum(
                1 for r in results 
                if r["ml_confidence"] >= threshold and r["ml_top1_correct"]
            )
            coverage = covered / len(confidences) if confidences else 0
            accuracy_at_threshold = correct_at_threshold / covered if covered > 0 else 0
            print(f"  Threshold {threshold:.1f}: Coverage={coverage:.1%}, Accuracy={accuracy_at_threshold:.1%}")
    
    # Save results
    output_path = HERE / "broken_english_evaluation_results.csv"
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_path, index=False)
    print(f"\n💾 Results saved to: {output_path}")
    
    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()


