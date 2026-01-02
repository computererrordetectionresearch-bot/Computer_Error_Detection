"""
Create comprehensive test dataset with 100,000 different PC error examples.
Includes single and multiple error type scenarios.
"""

from pathlib import Path
import pandas as pd
import sys
import io
import random
import itertools

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

# Error type templates with variations
ERROR_TEMPLATES = {
    # Hardware Issues
    "GPU Overheat": [
        "GPU overheating during games", "Graphics card too hot", "GPU fan not working",
        "GPU temperature high", "Graphics card overheating", "GPU thermal issue",
        "GPU hot when gaming", "Graphics card fan loud", "GPU overheat warning",
        "GPU shutdown due to heat", "Graphics card thermal throttle", "GPU cooling problem",
    ],
    "CPU Overheat": [
        "CPU overheating", "Processor too hot", "CPU fan not spinning",
        "CPU temperature high", "Processor overheating", "CPU thermal issue",
        "CPU hot always", "Processor fan loud", "CPU overheat warning",
        "CPU shutdown due to heat", "Processor thermal throttle", "CPU cooling problem",
    ],
    "PSU / Power Issue": [
        "PC not turning on", "No power at all", "Power button not working",
        "PC dead after power cut", "PC start then off", "PC restart again and again",
        "PC shutdown suddenly", "PC start only sometimes", "Laptop charging light blink",
        "PC power flicker", "PC dead after rain", "PC start noise then off",
    ],
    "RAM Upgrade": [
        "Need more RAM", "RAM not enough", "Memory upgrade needed",
        "RAM full", "Memory insufficient", "RAM performance issue",
        "Need more memory", "RAM outdated", "Memory upgrade required",
        "RAM not detected", "PC beep sound", "Memory error message",
    ],
    "SSD Upgrade": [
        "Need faster storage", "SSD upgrade needed", "Storage too slow",
        "SSD performance", "Storage upgrade required", "SSD not fast enough",
        "PC slow boot", "PC slow opening files", "PC slow loading programs",
    ],
    "GPU Upgrade": [
        "Need better graphics card", "GPU too weak", "Graphics card upgrade needed",
        "GPU bottleneck", "Graphics not good enough", "GPU performance issue",
        "Low FPS problem", "Game lag graphics", "Graphics card not detect",
    ],
    "No Display / No Signal": [
        "Screen black PC on", "No display", "Monitor no signal",
        "PC no signal", "PC on blank screen", "PC no display HDMI",
        "PC no display VGA", "PC no signal display", "Monitor not detected",
    ],
    "Blue Screen (BSOD)": [
        "PC blue screen", "Windows crash suddenly", "BSOD error",
        "Blue screen of death", "Stop code error", "Blue screen crash",
        "Windows error screen", "Windows crash loop", "Laptop error screen",
    ],
    "Windows Boot Failure": [
        "PC not boot", "Windows not starting", "Boot failure",
        "PC stuck on logo", "PC stuck loading", "Computer stuck booting",
        "PC not start after update", "PC stuck startup repair", "PC stuck BIOS",
    ],
    "Slow Performance": [
        "PC very slow", "Computer slow", "System slow",
        "PC lag always", "PC slow after update", "PC slow performance",
        "System slow overall", "PC very unresponsive", "System sluggish",
    ],
    "Wi-Fi Adapter Upgrade": [
        "No internet on PC", "WiFi not working", "Internet not working",
        "WiFi connected no internet", "PC not detect WiFi", "WiFi disconnect always",
        "Internet slow only PC", "WiFi very slow PC", "PC can't connect WiFi",
    ],
    "USB / Port Issue": [
        "USB not working", "USB port broken", "USB device not recognized",
        "USB port not working", "USB not detected", "USB cable issue",
        "Port not working", "USB port damaged", "USB connection issue",
    ],
    "Phone Connection Issue": [
        "Phone not connecting", "Phone not detected", "Phone connection problem",
        "Phone not recognized", "Phone USB issue", "Phone not showing",
    ],
    "General Repair": [
        "PC not working", "Computer problem", "PC issue",
        "Something wrong PC", "PC problem unknown", "PC malfunction",
    ],
}

# Multi-error type combinations (common scenarios)
MULTI_ERROR_COMBINATIONS = [
    # Overheating + Performance
    (["CPU Overheat", "Slow Performance"], [
        "PC very slow and CPU overheating", "Computer slow and processor hot",
        "System slow CPU temperature high", "PC lagging and CPU fan loud",
    ]),
    (["GPU Overheat", "Slow Performance"], [
        "GPU overheating and games lagging", "Graphics card hot and low FPS",
        "GPU temperature high and slow performance", "Graphics overheating and system slow",
    ]),
    # Power + Boot
    (["PSU / Power Issue", "Windows Boot Failure"], [
        "PC not turning on and not booting", "Power issue and boot failure",
        "PC dead and cannot start Windows", "Power problem and boot error",
    ]),
    # Display + GPU
    (["No Display / No Signal", "GPU Upgrade"], [
        "No display and graphics card issue", "Screen black and GPU problem",
        "Monitor no signal and graphics not working", "No display and GPU not detected",
    ]),
    # RAM + Performance
    (["RAM Upgrade", "Slow Performance"], [
        "PC slow and need more RAM", "System slow and memory insufficient",
        "Computer lagging and RAM full", "PC slow performance and RAM not enough",
    ]),
    # SSD + Boot
    (["SSD Upgrade", "Windows Boot Failure"], [
        "PC slow boot and boot failure", "Storage slow and cannot boot",
        "SSD slow and Windows not starting", "Boot device slow and boot error",
    ]),
    # BSOD + Boot
    (["Blue Screen (BSOD)", "Windows Boot Failure"], [
        "Blue screen and cannot boot", "BSOD error and boot failure",
        "Windows crash and not starting", "Blue screen and boot loop",
    ]),
    # WiFi + USB
    (["Wi-Fi Adapter Upgrade", "USB / Port Issue"], [
        "WiFi not working and USB ports broken", "Internet issue and USB not detected",
        "Network problem and USB port issue", "WiFi adapter and USB connection problem",
    ]),
    # Triple combinations
    (["CPU Overheat", "Slow Performance", "RAM Upgrade"], [
        "PC slow CPU hot and need more RAM", "System slow processor overheating and memory full",
        "Computer lagging CPU temperature high and RAM insufficient",
    ]),
    (["PSU / Power Issue", "Windows Boot Failure", "No Display / No Signal"], [
        "PC not turning on no display and boot failure", "Power issue no signal and cannot boot",
        "PC dead no display and boot error",
    ]),
]

def generate_single_error_samples():
    """Generate single error type samples."""
    rows = []
    error_types = list(ERROR_TEMPLATES.keys())
    
    # Generate ~80,000 single error samples
    samples_per_type = 80000 // len(error_types)
    
    for error_type in error_types:
        templates = ERROR_TEMPLATES[error_type]
        
        for i in range(samples_per_type):
            if i < len(templates):
                issue_text = templates[i]
            else:
                # Create variations
                base_template = random.choice(templates)
                variations = [
                    base_template,
                    base_template.lower(),
                    f"my {base_template.lower()}",
                    f"the {base_template.lower()}",
                    f"{base_template.lower()} problem",
                    f"{base_template.lower()} issue",
                    f"help {base_template.lower()}",
                    f"fix {base_template.lower()}",
                    f"{base_template.lower()} please",
                    f"computer {base_template.lower()}",
                    f"laptop {base_template.lower()}",
                    f"pc {base_template.lower()}",
                ]
                issue_text = random.choice(variations)
            
            rows.append({
                'user_text': issue_text,
                'error_type': error_type,
                'error_types': error_type,  # Single type
                'component_label': error_type,
                'source': 'test_dataset_single'
            })
    
    return rows

def generate_multi_error_samples():
    """Generate multi-error type samples."""
    rows = []
    
    # Generate ~20,000 multi-error samples
    samples_per_combination = 20000 // len(MULTI_ERROR_COMBINATIONS)
    
    for error_types, templates in MULTI_ERROR_COMBINATIONS:
        for i in range(samples_per_combination):
            if i < len(templates):
                issue_text = templates[i]
            else:
                # Create variations by combining templates from each error type
                parts = []
                for et in error_types:
                    if et in ERROR_TEMPLATES:
                        part = random.choice(ERROR_TEMPLATES[et])
                        parts.append(part)
                
                if parts:
                    # Combine in different ways
                    variations = [
                        " and ".join(parts),
                        ", ".join(parts),
                        " ".join(parts),
                        f"{parts[0]} also {parts[1] if len(parts) > 1 else ''}",
                        f"{parts[0]} plus {parts[1] if len(parts) > 1 else ''}",
                    ]
                    issue_text = random.choice(variations)
                else:
                    issue_text = " ".join(error_types)
            
            # Store multiple error types as comma-separated
            error_types_str = ", ".join(error_types)
            
            rows.append({
                'user_text': issue_text,
                'error_type': error_types[0],  # Primary type (first one)
                'error_types': error_types_str,  # All types
                'component_label': error_types[0],
                'source': 'test_dataset_multi'
            })
    
    return rows

def create_test_dataset():
    """Create test dataset with 100,000 error examples."""
    print("=" * 80)
    print("CREATING 100,000 ERROR TEST DATASET")
    print("=" * 80)
    
    print("\n[1/3] Generating single error type samples...")
    single_rows = generate_single_error_samples()
    print(f"Generated {len(single_rows)} single error samples")
    
    print("\n[2/3] Generating multi-error type samples...")
    multi_rows = generate_multi_error_samples()
    print(f"Generated {len(multi_rows)} multi-error samples")
    
    # Combine and shuffle
    print("\n[3/3] Combining and shuffling...")
    all_rows = single_rows + multi_rows
    random.shuffle(all_rows)
    
    # Limit to exactly 100,000
    all_rows = all_rows[:100000]
    
    df = pd.DataFrame(all_rows)
    
    print(f"\n{'='*80}")
    print(f"FINAL DATASET STATISTICS")
    print(f"{'='*80}")
    print(f"Total samples: {len(df)}")
    print(f"Single error samples: {len(df[df['source'] == 'test_dataset_single'])}")
    print(f"Multi-error samples: {len(df[df['source'] == 'test_dataset_multi'])}")
    
    print(f"\nError type distribution (primary):")
    print(df['error_type'].value_counts().head(15))
    
    # Save to CSV
    output_file = DATA_DIR / "test_100000_errors.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n{'='*80}")
    print(f"Test dataset saved to: {output_file}")
    print(f"{'='*80}")
    
    return df


if __name__ == "__main__":
    create_test_dataset()

