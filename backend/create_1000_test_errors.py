"""
Create comprehensive test dataset with 1000 different error examples.
Covers all error types with various phrasings and real-world variations.
"""

from pathlib import Path
import pandas as pd
import sys
import io
import random

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
        "GPU heat issue", "Graphics card temperature", "GPU fan spinning fast",
        "GPU overheat crash", "Graphics card hot", "GPU thermal paste",
        "GPU cooling fan", "Graphics overheating", "GPU temp high",
    ],
    "CPU Overheat": [
        "CPU overheating", "Processor too hot", "CPU fan not spinning",
        "CPU temperature high", "Processor overheating", "CPU thermal issue",
        "CPU hot always", "Processor fan loud", "CPU overheat warning",
        "CPU shutdown due to heat", "Processor thermal throttle", "CPU cooling problem",
        "CPU heat issue", "Processor temperature", "CPU fan spinning fast",
        "CPU overheat crash", "Processor hot", "CPU thermal paste",
        "CPU cooling fan", "Processor overheating", "CPU temp high",
        "PC very hot", "Laptop overheating", "System temperature high",
    ],
    "PSU / Power Issue": [
        "PC not turning on", "No power at all", "Power button not working",
        "PC dead after power cut", "PC start then off", "PC restart again and again",
        "PC shutdown suddenly", "PC start only sometimes", "Laptop charging light blink",
        "PC power flicker", "PC dead after rain", "PC start noise then off",
        "Laptop auto shutdown", "Computer power issue", "PC power delay",
        "PC auto shutdown", "PC no power button light", "PC power noise",
        "PC power surge damage", "Laptop not charging", "PC dead after voltage drop",
        "PC power unstable", "PC no power LED", "PC power click sound",
        "PC not start cold", "Laptop no power", "PC no power sometimes",
        "PC power off idle", "PC restart pressing power", "Laptop not detect charger",
    ],
    "Motherboard Issue": [
        "Motherboard not working", "Mobo problem", "Mainboard issue",
        "Motherboard dead", "Mobo failure", "Mainboard not detected",
        "Motherboard error", "Mobo damaged", "Mainboard problem",
        "Motherboard short circuit", "Mobo not booting", "Mainboard failure",
    ],
    "CPU Upgrade": [
        "Need faster processor", "CPU too slow", "Processor upgrade needed",
        "CPU bottleneck", "Processor not fast enough", "CPU performance issue",
        "Need better CPU", "Processor outdated", "CPU upgrade required",
    ],
    "GPU Upgrade": [
        "Need better graphics card", "GPU too weak", "Graphics card upgrade needed",
        "GPU bottleneck", "Graphics not good enough", "GPU performance issue",
        "Need better GPU", "Graphics card outdated", "GPU upgrade required",
        "Low FPS problem", "Game lag graphics", "Graphics card not detect",
    ],
    "RAM Upgrade": [
        "Need more RAM", "RAM not enough", "Memory upgrade needed",
        "RAM full", "Memory insufficient", "RAM performance issue",
        "Need more memory", "RAM outdated", "Memory upgrade required",
        "RAM not detected", "PC beep sound", "Memory error message",
        "RAM issue maybe", "Memory usage high", "RAM problem",
    ],
    "SSD Upgrade": [
        "Need faster storage", "SSD upgrade needed", "Storage too slow",
        "SSD performance", "Storage upgrade required", "SSD not fast enough",
        "Need better SSD", "Storage outdated", "SSD upgrade",
        "PC slow boot", "PC slow opening files", "PC slow loading programs",
        "PC slow file open", "PC slow copy files", "PC slow boot disk",
    ],
    "HDD Upgrade": [
        "Need more storage", "HDD full", "Hard drive upgrade needed",
        "HDD not enough space", "Storage full", "Hard drive upgrade required",
        "Need bigger HDD", "HDD outdated", "Storage upgrade",
    ],
    "Fan / Cooling Issue": [
        "Fan not working", "Cooling system problem", "Fan not spinning",
        "Fan broken", "Cooling issue", "Fan making noise",
        "Fan very loud", "Cooling problem PC", "Fan vibration noise",
        "Fan noisy always", "PC air flow bad", "PC cooling fail",
    ],
    "Thermal Paste Reapply": [
        "Thermal paste dried", "Need new thermal paste", "Thermal paste replacement",
        "CPU thermal paste", "GPU thermal paste", "Thermal paste issue",
    ],
    "Battery Replacement": [
        "Laptop battery dead", "Battery not holding charge", "Battery replacement needed",
        "Laptop battery not charging", "Battery swollen", "Battery replacement required",
        "Laptop dead battery", "Battery not detect", "Laptop battery issue",
    ],
    "Charging Port Issue": [
        "Laptop charging port broken", "Charging port not working", "DC jack issue",
        "Charging port loose", "DC jack broken", "Charging port damaged",
        "Laptop not detect charger", "Charging port problem", "DC jack replacement",
    ],
    
    # Display Issues
    "Monitor Issue": [
        "Monitor not working", "Display problem", "Screen issue",
        "Monitor flickering", "Lines on screen", "Screen white suddenly",
        "Display flicker random", "Monitor flicker screen", "Screen blink issue",
        "Monitor display issue", "Screen pixel issue", "Monitor no picture",
    ],
    "No Display / No Signal": [
        "Screen black PC on", "No display", "Monitor no signal",
        "PC no signal", "PC on blank screen", "PC no display HDMI",
        "PC no display VGA", "PC no signal display", "Monitor not detected",
        "PC stuck black screen", "Nothing show on monitor", "PC fan spin but no display",
        "PC light on but screen black", "PC on then blank", "Laptop no display but on",
    ],
    "Laptop Screen Repair": [
        "Laptop screen broken", "Screen cracked", "Laptop display damaged",
        "Screen repair needed", "Laptop screen issue", "Display repair",
        "Laptop screen black", "Screen not working", "Laptop display problem",
    ],
    "Display Cable Issue": [
        "HDMI cable not working", "Display cable broken", "VGA cable issue",
        "Display cable loose", "HDMI not working", "VGA not working",
    ],
    
    # System Issues
    "Blue Screen (BSOD)": [
        "PC blue screen", "Windows crash suddenly", "BSOD error",
        "Blue screen of death", "Stop code error", "Blue screen crash",
        "Windows error screen", "Windows crash loop", "Laptop error screen",
    ],
    "Windows Boot Failure": [
        "PC not boot", "Windows not starting", "Boot failure",
        "PC stuck on logo", "PC stuck loading", "Computer stuck booting",
        "PC not start after update", "PC stuck startup repair", "PC stuck BIOS",
        "PC boot loop", "PC fail to start", "System not booting",
        "PC stuck restart", "PC boot fail error", "PC boot fail random",
        "PC no boot device", "PC stuck repair loop", "PC stuck preparing repair",
        "PC stuck auto repair", "PC no boot after crash", "PC boot only BIOS",
    ],
    "OS Reinstall / Corrupted": [
        "Windows corrupted", "OS corrupted", "System corrupted message",
        "Windows reinstall needed", "OS reinstall required", "System corruption",
        "PC system corrupted", "Windows OS error", "Laptop OS error",
        "OS not working", "Windows OS crash", "Laptop OS broken",
    ],
    "BIOS Issue": [
        "BIOS problem", "BIOS error", "BIOS not working",
        "BIOS corrupted", "BIOS update needed", "BIOS issue",
        "PC stuck BIOS", "BIOS open only", "PC stuck BIOS logo",
    ],
    "Boot Device Error": [
        "Boot device not found", "No bootable device", "Boot device error",
        "Cannot find boot device", "Boot device missing", "Boot device problem",
    ],
    
    # Performance Issues
    "Slow Performance": [
        "PC very slow", "Computer slow", "System slow",
        "PC lag always", "PC slow after update", "PC slow performance",
        "System slow overall", "PC very unresponsive", "System sluggish",
        "PC delay everything", "PC slow suddenly", "PC slow after few minutes",
        "PC slow with internet", "PC slow with antivirus", "PC slow after software install",
        "PC slow with updates", "PC slow loading programs", "PC slow file explorer",
        "PC slow idle", "PC slow refresh", "PC slow shutdown",
    ],
    "System Freeze": [
        "PC freeze often", "System freeze", "PC hang always",
        "Everything freeze suddenly", "PC freeze randomly", "PC freeze idle",
        "PC freeze after hours", "PC freeze app open", "PC freeze copy files",
        "PC freeze desktop", "PC freeze startup", "PC freeze boot logo",
        "PC freeze gaming", "PC freeze updates", "PC freeze file save",
    ],
    "Application Crash": [
        "Apps crashing", "Programs crash", "Application error",
        "Software crash", "Program not responding", "App crash error",
        "Application freeze", "Program crash random", "App crash startup",
    ],
    
    # Software Issues
    "Virus / Malware": [
        "PC infected", "Virus detected", "Malware problem",
        "Computer virus", "Malware infection", "Virus removal needed",
        "PC slow after virus", "Malware scan needed", "Virus removal",
    ],
    "Driver Issue": [
        "Driver problem", "Driver error", "Driver not working",
        "Driver missing", "Driver outdated", "Driver conflict",
        "Display driver error", "Graphics driver fail", "Driver problem error",
        "Network driver missing", "Audio driver issue", "USB driver problem",
    ],
    "Software Conflict": [
        "Software conflict", "Programs conflict", "App conflict",
        "Software incompatible", "Programs not working together", "Software clash",
    ],
    "Windows Update Issue": [
        "Windows update fail", "Update not working", "Update error",
        "Windows update problem", "Update stuck", "Update failed",
        "PC restart after update", "Update causing issues", "Windows update broken",
    ],
    
    # Network Issues
    "Wi-Fi Adapter Upgrade": [
        "No internet on PC", "WiFi not working", "Internet not working",
        "WiFi connected no internet", "PC not detect WiFi", "WiFi disconnect always",
        "Internet slow only PC", "WiFi very slow PC", "PC can't connect WiFi",
        "WiFi keeps disconnect", "WiFi error PC", "WiFi not found",
        "Laptop no WiFi", "WiFi not turning on", "Network adapter error",
    ],
    "Ethernet Issue": [
        "Ethernet not working", "Ethernet cable not detect", "Ethernet connected no net",
        "Ethernet slow speed", "Ethernet not recognized", "Ethernet cable issue",
    ],
    "Network Cable Issue": [
        "Network cable broken", "Cable not working", "Network cable damaged",
        "Ethernet cable problem", "Cable loose", "Network cable issue",
    ],
    "Bluetooth Issue": [
        "Bluetooth not working", "Bluetooth not connecting", "Bluetooth device not found",
        "Bluetooth error", "Bluetooth problem", "Bluetooth not turning on",
    ],
    
    # Peripheral Issues
    "Keyboard Issue": [
        "Keyboard not working", "Keys not responding", "Keyboard broken",
        "Keyboard keys stuck", "Keyboard typing wrong", "Keyboard not detected",
        "PC on but keyboard dead", "Keyboard not working", "Keys not working",
    ],
    "Mouse Issue": [
        "Mouse not working", "Mouse not moving", "Mouse buttons not working",
        "Mouse cursor jumping", "Mouse not detected", "Mouse lag",
        "Mouse delay", "Mouse freeze", "Mouse not responding",
    ],
    "USB / Port Issue": [
        "USB not working", "USB port broken", "USB device not recognized",
        "USB port not working", "USB not detected", "USB cable issue",
        "Port not working", "USB port damaged", "USB connection issue",
    ],
    "Audio Issue": [
        "No sound", "Audio not working", "Sound problem",
        "Audio error", "No audio output", "Sound not working",
        "Audio driver issue", "Sound card problem", "Audio device not found",
    ],
    "Speaker Issue": [
        "Speakers not working", "No sound from speakers", "Speaker broken",
        "Speaker not detected", "Speaker problem", "Speaker not producing sound",
    ],
    "Microphone Issue": [
        "Microphone not working", "Mic not detected", "Microphone not picking up sound",
        "Mic problem", "Microphone error", "Mic not responding",
    ],
    "Webcam Issue": [
        "Webcam not working", "Camera not detected", "Webcam not showing",
        "Camera error", "Webcam problem", "Camera not responding",
    ],
    "Printer Issue": [
        "Printer not working", "Printer not printing", "Printer error",
        "Printer not detected", "Printer problem", "Printer not connecting",
    ],
    "Touchpad Issue": [
        "Touchpad not working", "Touchpad not responding", "Touchpad cursor jumping",
        "Touchpad not detected", "Touchpad problem", "Touchpad not moving",
    ],
    
    # Data & Recovery
    "Data Recovery": [
        "Lost files", "Deleted files recovery", "Data recovery needed",
        "Files deleted", "Data lost", "Recover deleted files",
        "File recovery", "Data recovery service", "Recover lost data",
    ],
    "File Corruption": [
        "Files corrupted", "File not opening", "Corrupted files",
        "File error", "Corruption issue", "Files damaged",
        "File read error", "Corrupted data", "File access error",
    ],
    "Partition Issue": [
        "Partition not found", "Partition error", "Disk partition missing",
        "Partition corrupted", "Partition not accessible", "Partition problem",
    ],
    
    # Phone/Device Issues
    "Phone Connection Issue": [
        "Phone not connecting", "Phone not detected", "Phone connection problem",
        "Phone not recognized", "Phone USB issue", "Phone not showing",
    ],
    "Device Not Recognized": [
        "Device not detected", "Device not recognized", "Device not showing",
        "Device error", "Device not found", "Device connection issue",
    ],
    
    # General
    "General Repair": [
        "PC not working", "Computer problem", "PC issue",
        "Something wrong PC", "PC problem unknown", "PC malfunction",
        "PC need repair", "Computer broken", "PC always error",
        "PC error detected", "PC fault detected", "PC problem detected",
        "PC not normal", "PC broken software", "PC fail system",
        "My PC not working properly", "PC need fixing", "System broken maybe",
    ],
    "Hardware Diagnostic": [
        "Hardware check needed", "System diagnostic", "Hardware test",
        "Component check", "Hardware inspection", "System check",
    ],
    "System Optimization": [
        "System optimization", "PC optimization", "Performance optimization",
        "System tune up", "PC cleanup", "System maintenance",
    ],
}


def create_test_dataset():
    """Create test dataset with 1000 error examples."""
    print("=" * 80)
    print("CREATING 1000 ERROR TEST DATASET")
    print("=" * 80)
    
    rows = []
    error_types = list(ERROR_TEMPLATES.keys())
    
    # Calculate samples per error type (distribute evenly, then add more to common types)
    samples_per_type = 1000 // len(error_types)  # ~20 per type
    remaining = 1000 % len(error_types)
    
    # Add more samples to common error types
    common_types = [
        "PSU / Power Issue", "Slow Performance", "Windows Boot Failure",
        "RAM Upgrade", "SSD Upgrade", "No Display / No Signal",
        "CPU Overheat", "GPU Overheat", "Driver Issue", "General Repair"
    ]
    
    for error_type in error_types:
        templates = ERROR_TEMPLATES[error_type]
        num_samples = samples_per_type
        
        # Add extra samples to common types
        if error_type in common_types:
            num_samples += 5
        
        # Add remaining samples to first few types
        if error_types.index(error_type) < remaining:
            num_samples += 1
        
        # Generate samples from templates
        for i in range(num_samples):
            if i < len(templates):
                # Use template directly
                issue_text = templates[i]
            else:
                # Create variation from random template
                base_template = random.choice(templates)
                # Add variations
                variations = [
                    base_template,
                    base_template.lower(),
                    base_template.upper()[:1] + base_template[1:].lower(),
                    f"my {base_template.lower()}",
                    f"the {base_template.lower()}",
                    f"{base_template.lower()} problem",
                    f"{base_template.lower()} issue",
                ]
                issue_text = random.choice(variations)
            
            rows.append({
                'user_text': issue_text,
                'error_type': error_type,
                'component_label': error_type,
                'source': 'test_dataset'
            })
    
    # Shuffle rows
    random.shuffle(rows)
    
    # Limit to exactly 1000
    rows = rows[:1000]
    
    df = pd.DataFrame(rows)
    
    print(f"\nCreated {len(df)} test samples")
    print(f"\nError type distribution:")
    print(df['error_type'].value_counts().head(20))
    
    # Save to CSV
    output_file = DATA_DIR / "test_1000_errors.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n{'='*80}")
    print(f"Test dataset saved to: {output_file}")
    print(f"{'='*80}")
    
    return df


if __name__ == "__main__":
    create_test_dataset()

