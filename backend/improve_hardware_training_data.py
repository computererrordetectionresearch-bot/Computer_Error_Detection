"""
Improve hardware recommender training data with real-world examples.
Adds diverse, natural language descriptions for each component type.
"""

from pathlib import Path
import pandas as pd
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

# Real-world training examples for each component
IMPROVED_TRAINING_DATA = {
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
        "Browser tabs closing automatically",
        "Out of memory error",
        "PC slow with Chrome open",
        "Computer slow when multitasking",
        "RAM usage at 100%",
    ],
    
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
        "Windows slow startup",
        "Loading slow",
        "Files slow to open",
        "Disk usage at 100%",
        "HDD very slow",
    ],
    
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
        "Frame drops in games",
        "Graphics card not powerful enough",
        "Gaming performance bad",
        "Video card upgrade needed",
    ],
    
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
        "PC shuts down instantly",
        "Immediate shutdown",
        "Random shutdown",
        "PC turns off randomly",
        "Power supply not working",
    ],
    
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
        "Processor bottleneck",
        "CPU not powerful enough",
    ],
    
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
        "Unstable WiFi",
        "WiFi disconnects frequently",
        "Internet drops",
        "Can't connect to WiFi",
    ],
    
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
        "CPU temperature very high",
        "Processor overheating",
    ],
    
    "GPU Cooler Upgrade": [
        "GPU overheating",
        "Graphics card too hot",
        "GPU temperature high",
        "GPU fan not working",
        "GPU thermal issue",
        "GPU hot when gaming",
        "Graphics card fan loud",
        "GPU overheat warning",
        "Graphics card overheating",
    ],
    
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
        "Screen flickering",
        "Lines on screen",
        "Display artifacts",
    ],
    
    "Thermal Paste Reapply": [
        "CPU overheating after years",
        "Thermal paste dried",
        "Need new thermal paste",
        "CPU temperature high old paste",
        "Thermal paste replacement",
        "CPU temp high need paste",
    ],
    
    "Power Cable Replacement": [
        "Power cable broken",
        "Cable not working",
        "Power cable loose",
        "Cable damaged",
        "Power cable issue",
        "Power cord broken",
    ],
    
    "Case Fan Upgrade": [
        "PC overheating",
        "System temperature high",
        "PC very hot",
        "Cooling not enough",
        "Fan not working",
        "Case fan broken",
        "PC cooling problem",
        "System overheating",
    ],
    
    "Laptop Battery Replacement": [
        "Laptop battery dead",
        "Battery not holding charge",
        "Laptop battery not charging",
        "Battery swollen",
        "Laptop dead battery",
        "Battery not detect",
        "Laptop battery issue",
    ],
    
    "Bluetooth Adapter": [
        "Bluetooth not working",
        "Bluetooth not connecting",
        "Bluetooth device not found",
        "Bluetooth error",
        "Bluetooth problem",
        "Can't connect Bluetooth",
    ],
    
    "USB Hub": [
        "USB ports not enough",
        "Need more USB ports",
        "USB devices not connecting",
        "USB port issue",
        "Not enough USB ports",
    ],
    
    "Router Upgrade": [
        "Internet slow",
        "WiFi range poor",
        "Router outdated",
        "Network slow",
        "WiFi signal weak",
        "Router not working well",
    ],
    
    "UPS Upgrade": [
        "PC shutdown during power cut",
        "Need backup power",
        "Power backup needed",
        "UPS not working",
        "Power outage protection needed",
    ],
    
    "Webcam Upgrade": [
        "Camera not working",
        "Webcam not working",
        "Laptop camera not working",
        "Lap camera not working",
        "Camera not detected",
        "Webcam not detected",
        "Camera not showing",
        "Webcam not showing",
        "Camera error",
        "Webcam error",
        "Camera problem",
        "Webcam problem",
        "Camera not responding",
        "Webcam not responding",
        "Camera broken",
        "Webcam broken",
        "No camera",
        "No webcam",
        "Camera missing",
        "Webcam missing",
        "Laptop camera broken",
        "Built-in camera not working",
        # Application-specific issues
        "Zoom camera not showing",
        "Zoom video not working",
        "Zoom can't see myself",
        "Zoom not showing my video",
        "Teams camera not working",
        "Teams video not showing",
        "Skype camera not working",
        "Skype video not working",
        "Video call camera not working",
        "Video call no video",
        "Meeting camera not showing",
        "Can't see myself in Zoom",
        "Can't see myself in Teams",
        "Camera not working in Zoom",
        "Camera not working in Teams",
        "Camera not working in Skype",
        "Video not working in Zoom",
        "Video not working in Teams",
        "No video in Zoom",
        "No video in Teams",
        "Zoom application not show my video",
        "Zoom application camera not working",
    ],
}


def create_improved_training_data():
    """Create improved training data with real-world examples."""
    print("=" * 80)
    print("CREATING IMPROVED HARDWARE TRAINING DATA")
    print("=" * 80)
    
    rows = []
    
    # Add improved examples
    for component, examples in IMPROVED_TRAINING_DATA.items():
        for example in examples:
            rows.append({
                'user_text': example,
                'component_label': component,
                'component_definition': f"{component} is a hardware component or upgrade relevant to computer performance or repair.",
                'why_useful': f"{component} helps resolve the problem by improving stability, performance, or fixing failing hardware.",
                'extra_explanation': f"{component} may be required based on the symptoms described."
            })
    
    df_new = pd.DataFrame(rows)
    
    print(f"\nCreated {len(df_new)} new training examples")
    print(f"\nComponent distribution:")
    print(df_new['component_label'].value_counts())
    
    # Load existing data
    existing_file = DATA_DIR / "hardware_component_dataset_merged.csv"
    if existing_file.exists():
        df_existing = pd.read_csv(existing_file)
        print(f"\n[INFO] Loaded {len(df_existing)} existing examples")
        
        # Normalize text for comparison (lowercase, strip)
        df_existing['text_normalized'] = df_existing['user_text'].astype(str).str.lower().str.strip()
        df_new['text_normalized'] = df_new['user_text'].astype(str).str.lower().str.strip()
        
        # Find new examples that don't exist in original (by normalized text)
        existing_texts = set(df_existing['text_normalized'].unique())
        df_new_unique = df_new[~df_new['text_normalized'].isin(existing_texts)]
        
        print(f"\n[INFO] {len(df_new_unique)} new unique examples (out of {len(df_new)})")
        
        # Drop normalized column before combining
        df_existing = df_existing.drop(columns=['text_normalized'])
        df_new_unique = df_new_unique.drop(columns=['text_normalized'])
        
        # Combine
        df_combined = pd.concat([df_existing, df_new_unique], ignore_index=True)
        
        print(f"\n[INFO] Combined dataset: {len(df_combined)} examples")
        print(f"   - Original: {len(df_existing)}")
        print(f"   - New: {len(df_new_unique)}")
        
        # Save combined
        output_file = DATA_DIR / "hardware_component_dataset_improved.csv"
        df_combined.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n{'='*80}")
        print(f"Improved training data saved to: {output_file}")
        print(f"{'='*80}")
        
        return df_combined
    else:
        # Save only new data
        output_file = DATA_DIR / "hardware_component_dataset_improved.csv"
        df_new.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n{'='*80}")
        print(f"New training data saved to: {output_file}")
        print(f"{'='*80}")
        
        return df_new


if __name__ == "__main__":
    create_improved_training_data()

