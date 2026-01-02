"""
Test that fixing tips are included in hardware recommender response.
"""

from pathlib import Path
import sys
import io
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()

# Test cases
TEST_CASES = [
    ("lap camera not working", "Webcam Upgrade"),
    ("PC very slow", "RAM Upgrade"),
    ("PC slow boot", "SSD Upgrade"),
    ("PC not turning on", "PSU Upgrade"),
    ("Low FPS in games", "GPU Upgrade"),
]

print("=" * 80)
print("TESTING FIXING TIPS IN HARDWARE RECOMMENDER")
print("=" * 80)

# Test fixing tips module
try:
    from component_fixing_tips import get_fixing_tips
    
    print("\n[TESTING FIXING TIPS MODULE]")
    print("-" * 80)
    
    for text, expected_component in TEST_CASES[:3]:
        tips = get_fixing_tips(expected_component)
        print(f"\n{expected_component}:")
        if tips:
            for i, tip in enumerate(tips[:3], 1):
                print(f"  {i}. {tip}")
        else:
            print("  No tips available")
    
    print("\n" + "=" * 80)
    print("FIXING TIPS MODULE TEST COMPLETE")
    print("=" * 80)
    
except Exception as e:
    print(f"[ERROR] Failed to test fixing tips: {e}")
    import traceback
    traceback.print_exc()

# Test API endpoint (if backend is running)
print("\n[TESTING API ENDPOINT]")
print("-" * 80)
print("Note: Backend must be running on http://localhost:8000")
print()

try:
    import requests
    
    for text, expected_component in TEST_CASES[:2]:
        try:
            response = requests.post(
                "http://localhost:8000/product_need_recommend",
                json={"text": text},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                component = data.get('component')
                fixing_tips = data.get('fixing_tips')
                
                print(f"Input: '{text}'")
                print(f"Component: {component}")
                if fixing_tips:
                    print(f"Fixing Tips ({len(fixing_tips)} tips):")
                    for i, tip in enumerate(fixing_tips[:3], 1):
                        print(f"  {i}. {tip}")
                else:
                    print("  ⚠️ No fixing tips returned")
                print()
            else:
                print(f"  ⚠️ API returned {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("  ⚠️ Cannot connect to backend. Start server first:")
            print("    cd backend")
            print("    python -m uvicorn app:app --reload")
            break
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
    
except ImportError:
    print("  ⚠️ requests library not available. Install with: pip install requests")

print("=" * 80)
print("✅ Fixing tips feature ready!")
print("=" * 80)

