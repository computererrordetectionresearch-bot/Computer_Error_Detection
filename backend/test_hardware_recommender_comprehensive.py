"""
Comprehensive test suite for hardware recommender.
Tests 500+ real-world scenarios to identify improvement areas.
"""

from pathlib import Path
import pandas as pd
import sys
import io
import json
from collections import defaultdict
from typing import Dict, List, Tuple

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

# Comprehensive test cases organized by component type
HARDWARE_TEST_CASES = {
    # RAM Upgrade
    "RAM Upgrade": [
        "PC very slow multitasking",
        "Computer lag when opening many programs",
        "PC freeze when running multiple apps",
        "Need more memory for video editing",
        "RAM not enough for gaming",
        "Memory full error",
        "PC slow with many tabs open",
        "Computer hang when switching apps",
        "Insufficient RAM warning",
        "PC slow after opening browser",
        "Memory usage always high",
        "PC lag multitask",
        "Need more RAM",
        "RAM full",
        "Memory insufficient",
    ],
    
    # SSD Upgrade
    "SSD Upgrade": [
        "PC slow boot time",
        "Computer takes long to start",
        "PC slow opening files",
        "Files take forever to open",
        "PC slow loading programs",
        "Computer slow file explorer",
        "PC slow copy files",
        "HDD making noise",
        "PC slow after startup",
        "Boot time very slow",
        "PC slow file access",
        "Storage slow",
        "Need faster storage",
        "SSD upgrade needed",
        "PC slow boot disk",
    ],
    
    # GPU Upgrade
    "GPU Upgrade": [
        "PC slow gaming",
        "Low FPS in games",
        "Graphics lag when gaming",
        "Game stuttering",
        "Need better graphics card",
        "GPU too weak for games",
        "Graphics card outdated",
        "PC lag gaming",
        "Game performance poor",
        "Graphics bottleneck",
        "GPU not good enough",
        "Need better GPU",
        "Low FPS problem",
        "Game lag graphics",
    ],
    
    # PSU Upgrade
    "PSU Upgrade": [
        "PC not turning on",
        "No power at all",
        "PC start then off",
        "PC shutdown suddenly",
        "Power supply making noise",
        "PC restart randomly",
        "PSU fan loud",
        "PC power issue",
        "Power supply failure",
        "PC dead after power cut",
        "No power",
        "PSU problem",
        "Power supply broken",
        "PC not start",
    ],
    
    # CPU Upgrade
    "CPU Upgrade": [
        "CPU too slow",
        "Processor not fast enough",
        "Need faster processor",
        "CPU bottleneck",
        "Processor outdated",
        "CPU performance issue",
        "Need better CPU",
        "Processor slow",
        "CPU upgrade required",
    ],
    
    # WiFi Adapter Upgrade
    "WiFi Adapter Upgrade": [
        "No internet on PC",
        "WiFi not working",
        "Internet not working",
        "WiFi connected no internet",
        "PC not detect WiFi",
        "WiFi disconnect always",
        "Internet slow only PC",
        "WiFi very slow PC",
        "PC can't connect WiFi",
        "WiFi keeps disconnect",
        "No internet",
        "WiFi error PC",
        "WiFi not found",
    ],
    
    # CPU Cooler Upgrade
    "CPU Cooler Upgrade": [
        "CPU overheating",
        "Processor too hot",
        "CPU temperature high",
        "CPU fan not working",
        "CPU thermal issue",
        "CPU hot always",
        "Processor fan loud",
        "PC very hot",
        "CPU cooling problem",
    ],
    
    # GPU Cooler Upgrade
    "GPU Cooler Upgrade": [
        "GPU overheating",
        "Graphics card too hot",
        "GPU temperature high",
        "GPU fan not working",
        "GPU thermal issue",
        "GPU hot when gaming",
        "Graphics card fan loud",
        "GPU overheat warning",
    ],
    
    # Monitor or GPU Check
    "Monitor or GPU Check": [
        "No display",
        "Screen black PC on",
        "Monitor no signal",
        "PC no signal",
        "PC on blank screen",
        "No display HDMI",
        "Fan spin no display",
        "PC stuck black screen",
        "Nothing show on monitor",
        "PC fan spin but no display",
    ],
    
    # Thermal Paste Reapply
    "Thermal Paste Reapply": [
        "CPU overheating after years",
        "Thermal paste dried",
        "Need new thermal paste",
        "CPU temperature high old paste",
        "Thermal paste replacement",
    ],
    
    # Power Cable Replacement
    "Power Cable Replacement": [
        "Power cable broken",
        "Cable not working",
        "Power cable loose",
        "Cable damaged",
        "Power cable issue",
    ],
    
    # Case Fan Upgrade
    "Case Fan Upgrade": [
        "PC overheating",
        "System temperature high",
        "PC very hot",
        "Cooling not enough",
        "Fan not working",
        "Case fan broken",
        "PC cooling problem",
    ],
    
    # Laptop Battery Replacement
    "Laptop Battery Replacement": [
        "Laptop battery dead",
        "Battery not holding charge",
        "Laptop battery not charging",
        "Battery swollen",
        "Laptop dead battery",
        "Battery not detect",
    ],
    
    # Bluetooth Adapter
    "Bluetooth Adapter": [
        "Bluetooth not working",
        "Bluetooth not connecting",
        "Bluetooth device not found",
        "Bluetooth error",
        "Bluetooth problem",
    ],
    
    # USB Hub
    "USB Hub": [
        "USB ports not enough",
        "Need more USB ports",
        "USB devices not connecting",
        "USB port issue",
    ],
    
    # Router Upgrade
    "Router Upgrade": [
        "Internet slow",
        "WiFi range poor",
        "Router outdated",
        "Network slow",
        "WiFi signal weak",
    ],
    
    # UPS Upgrade
    "UPS Upgrade": [
        "PC shutdown during power cut",
        "Need backup power",
        "Power backup needed",
        "UPS not working",
    ],
}

# Multi-component scenarios (should recommend multiple components)
MULTI_COMPONENT_CASES = {
    "RAM Upgrade + SSD Upgrade": [
        "PC very slow overall",
        "Computer slow everything",
        "PC slow boot and multitask",
        "System slow all around",
    ],
    "PSU Upgrade + Power Cable Replacement": [
        "PC not turning on no power",
        "Power issue PC dead",
        "No power at all",
    ],
    "CPU Cooler Upgrade + Case Fan Upgrade": [
        "PC overheating always",
        "System temperature very high",
        "PC very hot all time",
    ],
    "GPU Upgrade + CPU Upgrade": [
        "Gaming performance poor",
        "Games lag and stutter",
        "Need better gaming PC",
    ],
}


def create_test_dataset():
    """Create comprehensive test dataset."""
    print("=" * 80)
    print("CREATING COMPREHENSIVE HARDWARE RECOMMENDER TEST DATASET")
    print("=" * 80)
    
    rows = []
    
    # Single component cases
    for component, test_cases in HARDWARE_TEST_CASES.items():
        for test_case in test_cases:
            rows.append({
                'user_text': test_case,
                'expected_component': component,
                'test_type': 'single_component'
            })
    
    # Multi-component cases
    for components_str, test_cases in MULTI_COMPONENT_CASES.items():
        components = [c.strip() for c in components_str.split('+')]
        for test_case in test_cases:
            rows.append({
                'user_text': test_case,
                'expected_component': components[0],  # Primary
                'expected_related': ','.join(components[1:]) if len(components) > 1 else '',
                'test_type': 'multi_component'
            })
    
    df = pd.DataFrame(rows)
    
    print(f"\nCreated {len(df)} test cases")
    print(f"\nComponent distribution:")
    print(df['expected_component'].value_counts().head(15))
    
    # Save
    output_file = DATA_DIR / "hardware_recommender_test_cases.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n{'='*80}")
    print(f"Test dataset saved to: {output_file}")
    print(f"{'='*80}")
    
    return df


def test_hardware_recommender():
    """Test the hardware recommender on all test cases."""
    print("=" * 80)
    print("TESTING HARDWARE RECOMMENDER")
    print("=" * 80)
    
    test_file = DATA_DIR / "hardware_recommender_test_cases.csv"
    if not test_file.exists():
        print("Creating test dataset first...")
        create_test_dataset()
        test_file = DATA_DIR / "hardware_recommender_test_cases.csv"
    
    df = pd.read_csv(test_file)
    print(f"\n[INFO] Loaded {len(df)} test cases")
    
    # Import API function (simulate API call)
    try:
        import requests
        API_BASE = "http://localhost:8000"
        
        results = []
        correct = 0
        component_stats = defaultdict(lambda: {'correct': 0, 'total': 0, 'incorrect': []})
        
        print(f"\n[INFO] Testing hardware recommender...")
        print("Note: Backend must be running on http://localhost:8000\n")
        
        for idx, row in df.iterrows():
            text = row['user_text']
            expected = row['expected_component']
            
            try:
                response = requests.post(
                    f"{API_BASE}/product_need_recommend",
                    json={"text": text},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    predicted = data.get('component')
                    confidence = data.get('confidence', 0.0)
                    alternatives = data.get('alternatives', [])
                    
                    is_correct = predicted == expected
                    
                    component_stats[expected]['total'] += 1
                    if is_correct:
                        correct += 1
                        component_stats[expected]['correct'] += 1
                    else:
                        component_stats[expected]['incorrect'].append({
                            'text': text,
                            'expected': expected,
                            'predicted': predicted,
                            'confidence': confidence
                        })
                    
                    results.append({
                        'text': text,
                        'expected': expected,
                        'predicted': predicted,
                        'confidence': confidence,
                        'correct': is_correct,
                        'alternatives_count': len(alternatives)
                    })
                    
                    if (idx + 1) % 50 == 0:
                        print(f"  Processed {idx + 1}/{len(df)}... (Accuracy: {correct/(idx+1)*100:.1f}%)")
                else:
                    print(f"[ERROR] API returned {response.status_code} for: {text}")
                    
            except requests.exceptions.ConnectionError:
                print("\n[ERROR] Cannot connect to backend API.")
                print("Please start the backend server first:")
                print("  cd backend")
                print("  python -m uvicorn app:app --reload")
                return
            except Exception as e:
                print(f"[ERROR] Failed to test: {text} - {e}")
        
        # Calculate accuracy
        total = len(results)
        accuracy = (correct / total) * 100 if total > 0 else 0
        
        print(f"\n{'='*80}")
        print(f"OVERALL RESULTS")
        print(f"{'='*80}")
        print(f"Total Tested: {total}")
        print(f"Correct: {correct}")
        print(f"Incorrect: {total - correct}")
        print(f"Accuracy: {accuracy:.2f}%")
        
        # Per-component accuracy
        print(f"\n{'='*80}")
        print(f"PER-COMPONENT ACCURACY")
        print(f"{'='*80}")
        print(f"{'Component':<35} {'Accuracy':<15} {'Correct/Total'}")
        print(f"{'-'*80}")
        
        component_accuracies = []
        for component, stats in sorted(component_stats.items()):
            if stats['total'] > 0:
                comp_accuracy = (stats['correct'] / stats['total']) * 100
                component_accuracies.append((component, comp_accuracy, stats['correct'], stats['total']))
                print(f"{component:<35} {comp_accuracy:>6.2f}%        {stats['correct']}/{stats['total']}")
        
        # Worst performing components
        component_accuracies.sort(key=lambda x: x[1])
        worst = component_accuracies[:10]
        
        print(f"\n{'='*80}")
        print(f"WORST PERFORMING COMPONENTS (Top 10)")
        print(f"{'='*80}")
        for component, acc, correct, total in worst:
            print(f"{component:<35} {acc:>6.2f}% ({correct}/{total})")
        
        # Save incorrect predictions
        incorrect_df = pd.DataFrame([
            {
                'user_text': r['text'],
                'expected_component': r['expected'],
                'predicted_component': r['predicted'],
                'confidence': r['confidence'],
                'source': 'incorrect_prediction'
            }
            for r in results if not r['correct']
        ])
        
        if len(incorrect_df) > 0:
            incorrect_file = DATA_DIR / "hardware_recommender_incorrect.csv"
            incorrect_df.to_csv(incorrect_file, index=False, encoding='utf-8')
            print(f"\n{'='*80}")
            print(f"INCORRECT PREDICTIONS SAVED")
            print(f"{'='*80}")
            print(f"File: {incorrect_file}")
            print(f"Count: {len(incorrect_df)}")
        
        # Save summary
        summary_file = HERE / "hardware_recommender_test_results.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                'overall': {
                    'total': total,
                    'correct': correct,
                    'accuracy': accuracy
                },
                'per_component': {
                    k: {
                        'correct': v['correct'],
                        'total': v['total'],
                        'accuracy': (v['correct'] / v['total'] * 100) if v['total'] > 0 else 0
                    }
                    for k, v in component_stats.items()
                }
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print(f"Summary saved to: {summary_file}")
        print(f"{'='*80}")
        
    except ImportError:
        print("[INFO] requests library not available. Install with: pip install requests")
        print("[INFO] Test dataset created. Run backend and test manually.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        create_test_dataset()
    else:
        test_hardware_recommender()

