"""
Quick test of the retrained error detection model on sample real-world issues.
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
]


def test_model():
    """Test the model on sample issues."""
    print("=" * 80)
    print("QUICK TEST OF RETRAINED ERROR DETECTION MODEL")
    print("=" * 80)
    
    try:
        # Import after setting up encoding
        sys.path.insert(0, str(HERE))
        from app import detect_error_type_hybrid
        
        correct = 0
        total = len(TEST_CASES)
        
        print(f"\nTesting {total} sample issues...\n")
        
        for issue, expected in TEST_CASES:
            result = detect_error_type_hybrid(issue)
            predicted = result.get('label', 'None')
            confidence = result.get('confidence', 0.0)
            source = result.get('source', 'unknown')
            
            is_correct = predicted == expected
            if is_correct:
                correct += 1
                status = "✅"
            else:
                status = "❌"
            
            print(f"{status} Issue: '{issue}'")
            print(f"   Expected: {expected}")
            print(f"   Predicted: {predicted} (confidence: {confidence:.2f}, source: {source})")
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

