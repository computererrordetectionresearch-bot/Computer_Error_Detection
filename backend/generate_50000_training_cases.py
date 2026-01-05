"""
Generate 50,000 diverse training cases for product need model.
Includes both user-like natural language and technical descriptions.
"""

from pathlib import Path
import pandas as pd
import random
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()
OUTPUT_FILE = DATA_DIR / "hardware_component_dataset_50000.csv"

# Component patterns with diverse user expressions
COMPONENT_PATTERNS = {
    "RAM Upgrade": [
        "pc is slow when opening many programs",
        "computer freezes with multiple tabs open",
        "chrome tabs keep closing automatically",
        "need more memory for multitasking",
        "system runs out of memory",
        "browser tabs lagging",
        "photoshop runs very slow",
        "premiere pro crashes when editing",
        "not enough ram for my work",
        "memory usage is always high",
        "i want to speed up my pc",
        "pc very slow with many apps",
        "computer sluggish when multitasking",
        "out of memory errors",
        "tabs closing on their own",
        "ram is full",
        "low memory warning",
        "memory insufficient",
        "need more ram",
        "add more memory",
        "ram upgrade needed",
        "memory upgrade required",
        "not enough memory",
        "memory problems",
        "ram issues",
        "memory errors",
        "insufficient ram",
        "low ram",
        "ram full",
        "memory full",
    ],
    "SSD Upgrade": [
        "windows takes forever to boot",
        "pc boots very slowly",
        "files take long to open",
        "slow startup time",
        "disk usage at 100 percent",
        "loading times are terrible",
        "games take forever to load",
        "applications load slowly",
        "slow boot time",
        "startup is very slow",
        "takes minutes to start windows",
        "file transfers are slow",
        "hard drive is slow",
        "need faster storage",
        "boot time is too long",
    ],
    "GPU Upgrade": [
        "low fps in games",
        "gaming lag and stuttering",
        "frame rate drops while gaming",
        "graphics card not good enough",
        "games run at low fps",
        "need better graphics card",
        "video editing is slow",
        "gpu cannot handle new games",
        "graphics performance is poor",
        "fps drops during gaming",
        "gaming performance is bad",
        "low frame rate in games",
        "graphics card upgrade needed",
        "games stutter and lag",
        "need more powerful gpu",
    ],
    "CPU Upgrade": [
        "processor is too slow",
        "cpu cannot handle workload",
        "need faster processor",
        "cpu usage always at 100",
        "processor bottleneck",
        "cpu is outdated",
        "need better cpu",
        "processor not powerful enough",
        "cpu struggles with tasks",
        "processor upgrade needed",
    ],
    "PSU Upgrade": [
        "pc shuts down randomly",
        "computer turns off suddenly",
        "random shutdowns",
        "power supply not working",
        "pc wont turn on",
        "no power to computer",
        "power supply failure",
        "computer restarts by itself",
        "psu is failing",
        "need more power",
        "power supply upgrade needed",
        "random power cuts",
        "pc dies during gaming",
    ],
    "CPU Cooler Upgrade": [
        "cpu overheating",
        "processor too hot",
        "cpu temperature very high",
        "computer overheats",
        "cpu thermal throttling",
        "processor overheating",
        "need better cpu cooling",
        "cpu cooler not working",
        "processor running hot",
        "cpu temperature issues",
    ],
    "WiFi Adapter Upgrade": [
        "wifi keeps disconnecting",
        "internet connection unstable",
        "wifi not working properly",
        "wireless connection drops",
        "wifi adapter not working",
        "internet keeps dropping",
        "wifi signal is weak",
        "wireless adapter issues",
        "wifi connection problems",
        "need better wifi adapter",
    ],
    "Webcam Upgrade": [
        "camera not working",
        "webcam not detected",
        "laptop camera broken",
        "zoom camera not showing",
        "webcam error",
        "camera not responding",
        "video call camera issues",
        "webcam not working in zoom",
        "camera problem",
        "need new webcam",
    ],
    "Monitor Replacement": [
        "screen is broken",
        "monitor has dead pixels",
        "display is damaged",
        "screen cracked",
        "monitor not working",
        "display issues",
        "screen replacement needed",
        "monitor broken",
        "display damaged",
    ],
    "Monitor or GPU Check": [
        "no display on monitor",
        "black screen but pc running",
        "monitor shows no signal",
        "screen is black",
        "no image on display",
        "monitor blank screen",
        "display not working",
        "screen flickering",
        "monitor flickering",
    ],
    "Laptop RAM Upgrade": [
        "laptop is very slow",
        "laptop needs more memory",
        "laptop ram is full",
        "laptop multitasking slow",
        "laptop running out of memory",
        "laptop needs ram upgrade",
    ],
    "Laptop SSD Upgrade": [
        "laptop boots slowly",
        "laptop startup is slow",
        "laptop hard drive slow",
        "laptop needs ssd",
        "laptop loading slow",
    ],
    "NVMe SSD Upgrade": [
        "need faster nvme drive",
        "m2 ssd upgrade needed",
        "nvme drive slow",
        "pcie ssd upgrade",
        "m2 slot available",
    ],
    "Case Fan Upgrade": [
        "pc gets very hot",
        "computer overheating",
        "case temperature high",
        "need more case fans",
        "airflow is poor",
        "pc case too hot",
    ],
    "Router Upgrade": [
        "internet speed is slow",
        "wifi router old",
        "network speed poor",
        "router not working well",
        "need better router",
    ],
    "Microphone Upgrade": [
        "microphone not working",
        "mic not detected",
        "people cant hear me",
        "microphone issues",
        "mic problems",
    ],
    "UPS Upgrade": [
        "power outages damage pc",
        "need backup power",
        "power surge protection",
        "uninterrupted power supply",
        "power backup needed",
    ],
    "Laptop Battery Replacement": [
        "laptop battery dead",
        "battery not charging",
        "laptop battery swollen",
        "battery life very short",
        "laptop battery replacement",
    ],
    "Bluetooth Adapter": [
        "bluetooth not working",
        "cant connect bluetooth devices",
        "bluetooth adapter missing",
        "bluetooth connection issues",
        "need bluetooth adapter",
    ],
    "GPU Cooler Upgrade": [
        "gpu overheating",
        "graphics card too hot",
        "gpu temperature high",
        "gpu thermal issues",
        "graphics card overheating",
    ],
    "Thermal Paste Reapply": [
        "cpu temperature high",
        "thermal paste dried",
        "need to reapply thermal paste",
        "cpu overheating after years",
        "thermal paste replacement",
    ],
    "Power Cable Replacement": [
        "power cable broken",
        "power cord not working",
        "cable replacement needed",
        "power cable damaged",
    ],
    "HDMI Cable Replacement": [
        "hdmi cable not working",
        "display cable broken",
        "hdmi connection issues",
        "cable replacement needed",
    ],
    "USB Hub Upgrade": [
        "not enough usb ports",
        "need more usb connections",
        "usb hub needed",
        "usb ports insufficient",
    ],
    "Capture Card": [
        "need capture card for streaming",
        "video capture device needed",
        "streaming capture card",
        "recording gameplay",
    ],
    "Audio Issue": [
        "no sound on computer",
        "audio not working",
        "sound card issues",
        "speakers not working",
    ],
    "Keyboard Upgrade": [
        "keyboard not working",
        "keys not responding",
        "keyboard broken",
        "need new keyboard",
    ],
    "Mouse Upgrade": [
        "mouse not working",
        "mouse cursor lagging",
        "mouse broken",
        "need new mouse",
    ],
}

def generate_user_like_texts(component, base_patterns, count):
    """Generate user-like natural language variations."""
    texts = []
    variations = [
        "i {text}",
        "my {text}",
        "my pc {text}",
        "my computer {text}",
        "i want to {text}",
        "i need to {text}",
        "help with {text}",
        "problem: {text}",
        "issue: {text}",
        "{text} please help",
        "how to fix {text}",
        "what to do about {text}",
        "having trouble with {text}",
        "experiencing {text}",
        "my system {text}",
        "pc {text}",
        "computer {text}",
        "laptop {text}",
        "need help {text}",
        "can't {text}",
        "unable to {text}",
    ]
    
    # Generate from base patterns
    for pattern in base_patterns:
        texts.append(pattern)
        for var in variations:
            try:
                texts.append(var.format(text=pattern))
            except:
                texts.append(f"{var} {pattern}")
    
    # Add numbered variations
    num = 0
    while len(texts) < count and num < 10000:
        base = random.choice(base_patterns)
        var = random.choice(variations)
        try:
            new_text = var.format(text=base)
        except:
            new_text = f"{var} {base}"
        # Add slight variations
        if num % 10 == 0:
            new_text = new_text.replace("very", "extremely")
        elif num % 10 == 1:
            new_text = new_text.replace("very", "really")
        elif num % 10 == 2:
            new_text = new_text.replace("not", "doesn't")
        texts.append(new_text)
        num += 1
    
    return list(set(texts))[:count]  # Remove duplicates and limit

def generate_technical_texts(component, base_patterns, count):
    """Generate technical/formal descriptions."""
    texts = []
    technical_prefixes = [
        "system experiencing {text}",
        "device showing symptoms of {text}",
        "hardware issue: {text}",
        "component failure: {text}",
        "diagnosis: {text}",
        "symptom: {text}",
        "error: {text}",
    ]
    
    for pattern in base_patterns:
        texts.append(pattern)
        for prefix in technical_prefixes[:2]:
            texts.append(prefix.format(text=pattern))
    
    while len(texts) < count:
        base = random.choice(base_patterns)
        prefix = random.choice(technical_prefixes)
        texts.append(prefix.format(text=base))
    
    return texts[:count]

def generate_50000_cases():
    """Generate 50,000 diverse training cases."""
    print("=" * 80)
    print("GENERATING 50,000 TRAINING CASES")
    print("=" * 80)
    
    rows = []
    total_needed = 50000
    components = list(COMPONENT_PATTERNS.keys())
    
    # Calculate samples per component (weighted by importance)
    # Increased weights to generate more samples
    weights = {
        "RAM Upgrade": 0.18,
        "SSD Upgrade": 0.15,
        "GPU Upgrade": 0.15,
        "PSU Upgrade": 0.10,
        "CPU Cooler Upgrade": 0.08,
        "WiFi Adapter Upgrade": 0.07,
        "Webcam Upgrade": 0.07,
        "Monitor Replacement": 0.06,
        "Monitor or GPU Check": 0.06,
        "CPU Upgrade": 0.05,
        "Laptop RAM Upgrade": 0.04,
        "Laptop SSD Upgrade": 0.04,
        "NVMe SSD Upgrade": 0.04,
        "Case Fan Upgrade": 0.03,
        "Router Upgrade": 0.03,
        "Microphone Upgrade": 0.03,
        "UPS Upgrade": 0.02,
        "Laptop Battery Replacement": 0.02,
        "Bluetooth Adapter": 0.02,
        "GPU Cooler Upgrade": 0.02,
        "Thermal Paste Reapply": 0.02,
        "Power Cable Replacement": 0.02,
        "HDMI Cable Replacement": 0.02,
        "USB Hub Upgrade": 0.02,
        "Capture Card": 0.02,
        "Audio Issue": 0.02,
        "Keyboard Upgrade": 0.02,
        "Mouse Upgrade": 0.02,
    }
    
    # Generate cases for each component
    for component in components:
        weight = weights.get(component, 0.01)
        count = int(total_needed * weight)
        base_patterns = COMPONENT_PATTERNS[component]
        
        # 60% user-like, 40% technical
        user_count = int(count * 0.6)
        tech_count = count - user_count
        
        # Generate user-like texts
        user_texts = generate_user_like_texts(component, base_patterns, user_count)
        for text in user_texts:
            if text and len(text.strip()) > 3:
                rows.append({
                    'user_text': text.strip(),
                    'component_label': component
                })
        
        # Generate technical texts
        tech_texts = generate_technical_texts(component, base_patterns, tech_count)
        for text in tech_texts:
            if text and len(text.strip()) > 3:
                rows.append({
                    'user_text': text.strip(),
                    'component_label': component
                })
    
    # Add random variations to reach exactly 50,000
    variation_templates = [
        "i {base}",
        "my {base}",
        "help {base}",
        "{base} issue",
        "{base} problem",
        "having {base}",
        "experiencing {base}",
        "trouble with {base}",
        "need {base}",
        "want {base}",
        "can't {base}",
        "unable to {base}",
        "my pc {base}",
        "my computer {base}",
        "my laptop {base}",
        "pc {base}",
        "computer {base}",
        "laptop {base}",
    ]
    
    # Add more variations with modifiers
    modifiers = ["", "very ", "really ", "extremely ", "too ", "always ", "constantly "]
    
    seen = set()
    num = 0
    while len(rows) < total_needed and num < 200000:
        component = random.choice(components)
        base_patterns = COMPONENT_PATTERNS[component]
        base = random.choice(base_patterns)
        
        # Try different variation strategies
        if num % 3 == 0:
            template = random.choice(variation_templates)
            modifier = random.choice(modifiers)
            try:
                variation = template.format(base=f"{modifier}{base}")
            except:
                variation = f"{template} {modifier}{base}"
        elif num % 3 == 1:
            variation = f"{random.choice(['i', 'my', 'the', 'this'])} {base}"
        else:
            variation = f"{base} {random.choice(['issue', 'problem', 'error', 'fault'])}"
        
        # Add unique identifier to ensure diversity
        key = (variation.lower().strip(), component)
        if key not in seen and len(variation.strip()) > 5:
            seen.add(key)
            rows.append({
                'user_text': variation.strip(),
                'component_label': component
            })
        num += 1
    
    # Trim to exactly 50,000
    rows = rows[:total_needed]
    
    df = pd.DataFrame(rows)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['user_text', 'component_label'])
    
    print(f"\nGenerated {len(df)} unique training cases")
    print(f"\nComponent distribution:")
    print(df['component_label'].value_counts())
    
    return df

if __name__ == "__main__":
    df = generate_50000_cases()
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"\n[SUCCESS] Training data saved to: {OUTPUT_FILE}")

