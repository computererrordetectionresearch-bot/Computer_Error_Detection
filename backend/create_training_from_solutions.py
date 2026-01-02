"""
Create training data from real-world issues with solutions.
Maps issues to appropriate error types.
"""

from pathlib import Path
import pandas as pd
import sys
import io
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

# Parse issues from the text
ISSUES_TEXT = """
POWER & STARTUP (1–100)
PC not turning on → Check power cable and wall socket
No power at all → Try different power outlet
Power button not working → Check cabinet power switch cable
PC dead after power cut → Test power supply
PC start then off → Power supply may be faulty
PC restart again and again → Check RAM seating
PC stuck black screen → Check monitor cable
Fan spin no display → Reseat RAM and GPU
Laptop not start → Remove battery and try charger
PC stuck on logo → Reset BIOS
PC no signal → Try different display cable
PC beep sound → RAM problem, clean and reseat
PC start slow then freeze → Check disk health
PC off suddenly → Overheating, clean fans
PC start only sometimes → Loose power cable
Laptop charging light blink → Charger or battery issue
PC not boot → Repair Windows startup
PC boot loop → Disable auto restart
PC on but keyboard dead → USB or motherboard issue
PC stuck loading → Check SSD/HDD
PC restart on login → Driver or RAM issue
PC no response → Hard reset system
PC power flicker → Use voltage stabilizer
PC dead after rain → PSU damaged
PC start noise then off → PSU fan issue
PC stuck BIOS → Reset CMOS
PC no display HDMI → Change input source
Laptop not waking → Disable fast startup
PC fail start → Boot repair tool
PC not shutdown → Force shutdown
Laptop battery not charging → Replace battery
PC power delay → PSU aging
PC auto shutdown → Thermal issue
PC no power button light → Motherboard issue
PC freeze startup → Check disk errors
PC restart after update → Rollback update
PC no boot device → Set correct boot drive
PC stuck repair loop → Startup repair
Laptop dead battery → Replace battery
PC crash startup → Safe mode boot
PC off when press power → Short circuit issue
PC not start after clean → Check cables
PC power noise → PSU fan problem
PC stuck welcome screen → Corrupt system files
PC on blank screen → GPU or RAM issue
Laptop power drain fast → Calibrate battery
PC no power after move → Loose cables
PC start but no OS → Install OS
PC freeze BIOS → Update BIOS
PC no boot beep → Motherboard issue
Laptop not turn on → Charger fault
PC stuck spinning dots → Windows repair
PC restart while boot → RAM or PSU
PC not respond startup → Check SSD
PC dead after voltage drop → PSU replace
PC start slow → Disable startup apps
PC power surge damage → Surge protector needed
Laptop auto off → Overheating
PC not boot USB → Enable boot menu
PC freeze logo → Disk corruption
PC power unstable → Replace PSU
PC no boot after upgrade → BIOS reset
PC no power LED → Motherboard check
Laptop blink screen no start → RAM issue
PC start then blank → GPU driver issue
PC no boot after RAM → RAM compatibility
PC stuck preparing repair → Disk check
PC no display VGA → Try HDMI
Laptop not start after sleep → Disable hibernate
PC power click sound → PSU fault
PC not start cold → PSU weak
PC freeze boot → SSD firmware
Laptop no power → DC jack issue
PC stuck restart → Windows repair
PC start then blue screen → Driver conflict
PC boot fail error → Reinstall OS
Laptop not detect charger → Replace charger
PC no display after GPU → Power cable missing
PC start fan loud → Dust issue
PC fail POST → Hardware issue
PC boot only BIOS → OS missing
PC stuck safe mode → Driver uninstall
Laptop no power response → Power board issue
PC stuck loading bar → System corruption
PC not boot SSD → Check SATA mode
PC power drain fast → PSU inefficient
PC no power sometimes → Loose socket
Laptop start then off → Thermal shutdown
PC no startup sound → Speaker unplugged
PC stuck auto repair → Disk issue
PC boot fail random → RAM error
Laptop boot black → GPU driver reset
PC start with error → Repair OS
PC power off idle → Power settings
PC stuck BIOS logo → BIOS update
PC restart pressing power → Short circuit
Laptop no display but on → Screen cable
PC no boot after crash → Startup repair
PC freeze boot logo → SSD failing
PC not working → Full system check

PERFORMANCE / SLOW (101–200)
PC very slow → Add RAM
PC lag always → Disable background apps
Laptop slow boot → SSD upgrade
PC freeze often → Check RAM
PC slow after update → Rollback update
PC lag typing → High CPU usage
PC slow browsing → Malware scan
PC hang multitask → Insufficient RAM
PC slow file open → HDD slow
Laptop lag video → Update graphics driver
PC slow startup → Disable startup apps
PC freeze idle → Power plan issue
PC lag mouse → USB driver
PC slow copy files → Disk health
PC delay click → High disk usage
PC slow gaming → GPU bottleneck
Laptop slow charging → Power plan
PC lag audio → Audio driver
PC slow internet apps → Network driver
PC freeze scroll → GPU driver
PC stutter random → Background updates
Laptop slow multitask → Add RAM
PC lag when hot → Clean cooling
PC freeze browser → Browser cache
PC slow after install → Remove bloatware
PC lag opening apps → SSD space low
PC hang heavy work → Thermal throttling
PC slow response → CPU high load
Laptop lag battery → Power saving mode
PC freeze updates → Disk error
PC lag USB → USB power issue
PC slow after sleep → Driver reload
PC stutter typing → CPU spike
PC lag on boot → Startup services
PC freeze gaming → GPU overheat
Laptop lag video call → CPU load
PC slow with antivirus → Exclusions
PC lag after long use → Restart system
PC slow file explorer → Disk indexing
PC stutter animation → GPU settings
PC lag window move → Graphics driver
PC freeze system tray → Explorer restart
Laptop slow wake → SSD firmware
PC lag zoom calls → RAM usage
PC slow idle → Background sync
PC hang copy paste → Disk cache
PC stutter mouse → Polling rate
PC slow login → User profile issue
Laptop lag sound → Audio buffer
PC slow install apps → Disk speed
PC lag multitask → CPU limit
PC freeze after hours → Memory leak
PC slow refresh → GPU driver
Laptop slow render → Thermal throttle
PC stutter browser → Extensions overload
PC lag typing delay → CPU spike
PC slow shutdown → Background apps
Laptop lag resume → Hibernate issue
PC freeze antivirus scan → Disk issue
PC slow UI → GPU acceleration
PC lag updates → Disk usage
Laptop slow charging mode → Low power
PC freeze app open → RAM shortage
PC slow windows load → SSD health
PC lag drag drop → Graphics issue
PC stutter gaming low FPS → GPU limit
Laptop lag zoom → Webcam driver
PC slow extract files → Disk speed
PC lag printing → Driver issue
PC freeze multitask → Upgrade RAM
PC slow network apps → DNS issue
Laptop lag boot → Too many apps
PC stutter scrolling → Display driver
PC lag with USB drive → USB speed
PC slow after virus → Malware removal
PC freeze file save → Disk error
PC lag brightness → GPU driver
Laptop slow IDE → RAM insufficient
PC stutter idle → Power plan
PC lag audio video → Codec issue
PC slow boot HDD → Upgrade SSD
PC freeze apps → Check RAM
Laptop lag heavy apps → Thermal issue
PC slow task manager → CPU load
PC lag start menu → Windows index
PC freeze copy files → Disk check
Laptop slow after update → Rollback
PC lag animations → Disable effects
PC slow internet apps → Proxy issue
PC freeze desktop → Explorer restart
PC stutter startup → Disable services
Laptop lag drivers → Update drivers
PC slow search → Index rebuild
PC lag switching apps → RAM shortage
PC freeze notifications → Windows bug
PC slow refresh rate → Display settings
Laptop lag compile → CPU overheating
PC stutter browser video → GPU decode
PC slow app launch → SSD nearly full
PC very slow → System optimization
"""

# Map solutions to error types
SOLUTION_TO_ERROR_TYPE = {
    # Power/Startup issues
    "power": "PSU / Power Issue",
    "power supply": "PSU / Power Issue",
    "PSU": "PSU / Power Issue",
    "charger": "PSU / Power Issue",
    "battery": "PSU / Power Issue",
    "power cable": "PSU / Power Issue",
    "voltage": "PSU / Power Issue",
    "surge": "PSU / Power Issue",
    
    # Boot/Startup issues
    "boot": "Windows Boot Failure",
    "startup": "Windows Boot Failure",
    "repair": "Windows Boot Failure",
    "BIOS": "Windows Boot Failure",
    "OS": "OS Reinstall / Corrupted",
    "windows": "Windows Boot Failure",
    "reinstall": "OS Reinstall / Corrupted",
    
    # Display issues
    "display": "No Display / No Signal",
    "monitor": "Monitor Issue",
    "screen": "No Display / No Signal",
    "HDMI": "No Display / No Signal",
    "VGA": "No Display / No Signal",
    "GPU": "GPU Upgrade",
    "graphics": "GPU Upgrade",
    "driver": "Driver Issue",
    
    # RAM issues
    "RAM": "RAM Upgrade",
    "ram": "RAM Upgrade",
    "memory": "RAM Upgrade",
    "RAM seating": "RAM Upgrade",
    "RAM compatibility": "RAM Upgrade",
    "RAM error": "RAM Upgrade",
    
    # Storage issues
    "SSD": "SSD Upgrade",
    "HDD": "SSD Upgrade",
    "disk": "SSD Upgrade",
    "storage": "SSD Upgrade",
    "SATA": "SSD Upgrade",
    
    # Performance issues
    "slow": "Slow Performance",
    "lag": "Slow Performance",
    "freeze": "Slow Performance",
    "hang": "Slow Performance",
    "stutter": "Slow Performance",
    
    # Overheating
    "overheat": "CPU Overheat",
    "thermal": "CPU Overheat",
    "cooling": "CPU Overheat",
    "fan": "CPU Overheat",
    "dust": "CPU Overheat",
    
    # General
    "system": "General Repair",
    "hardware": "General Repair",
    "motherboard": "General Repair",
    "USB": "USB / Port Issue",
    "network": "Wi-Fi Adapter Upgrade",
    "internet": "Wi-Fi Adapter Upgrade",
    "WiFi": "Wi-Fi Adapter Upgrade",
}


def parse_issues():
    """Parse issues from text and map to error types."""
    rows = []
    
    # Split by lines
    lines = ISSUES_TEXT.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or '→' not in line:
            continue
        
        # Extract issue and solution
        parts = line.split('→')
        if len(parts) != 2:
            continue
        
        issue = parts[0].strip()
        solution = parts[1].strip().lower()
        
        # Skip category headers
        if issue.startswith('POWER') or issue.startswith('PERFORMANCE'):
            continue
        
        # Determine error type from solution
        error_type = "General Repair"  # Default
        
        # Check solution keywords
        for keyword, error in SOLUTION_TO_ERROR_TYPE.items():
            if keyword.lower() in solution:
                error_type = error
                break
        
        # Also check issue text for better mapping
        issue_lower = issue.lower()
        if any(kw in issue_lower for kw in ['not turning on', 'no power', 'power button', 'dead', 'power cut']):
            error_type = "PSU / Power Issue"
        elif any(kw in issue_lower for kw in ['not boot', 'boot loop', 'stuck', 'logo', 'loading', 'startup']):
            error_type = "Windows Boot Failure"
        elif any(kw in issue_lower for kw in ['no display', 'black screen', 'no signal', 'blank screen']):
            error_type = "No Display / No Signal"
        elif any(kw in issue_lower for kw in ['beep', 'RAM', 'memory']):
            error_type = "RAM Upgrade"
        elif any(kw in issue_lower for kw in ['slow', 'lag', 'freeze', 'hang', 'stutter']):
            if 'boot' in issue_lower or 'startup' in issue_lower:
                error_type = "SSD Upgrade"
            elif 'gaming' in issue_lower or 'GPU' in issue_lower:
                error_type = "GPU Upgrade"
            elif 'multitask' in issue_lower or 'RAM' in solution:
                error_type = "RAM Upgrade"
            else:
                error_type = "Slow Performance"
        elif any(kw in issue_lower for kw in ['hot', 'overheat', 'thermal', 'fan', 'cooling']):
            error_type = "CPU Overheat"
        elif any(kw in issue_lower for kw in ['blue screen', 'BSOD', 'crash']):
            error_type = "Blue Screen (BSOD)"
        elif any(kw in issue_lower for kw in ['internet', 'WiFi', 'network']):
            error_type = "Wi-Fi Adapter Upgrade"
        elif any(kw in issue_lower for kw in ['driver', 'GPU driver', 'graphics driver']):
            error_type = "Driver Issue"
        
        rows.append({
            'user_text': issue,
            'error_type': error_type,
            'component_label': error_type,
            'source': 'real_world_solutions'
        })
    
    return rows


def create_training_csv():
    """Create training data CSV."""
    print("=" * 80)
    print("CREATING TRAINING DATA FROM ISSUES WITH SOLUTIONS")
    print("=" * 80)
    
    rows = parse_issues()
    df = pd.DataFrame(rows)
    
    print(f"\nCreated {len(df)} training samples")
    print(f"\nError type distribution:")
    print(df['error_type'].value_counts())
    
    # Save to CSV
    output_file = DATA_DIR / "real_world_solutions_training_data.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n{'='*80}")
    print(f"Training data saved to: {output_file}")
    print(f"{'='*80}")
    
    return df


if __name__ == "__main__":
    create_training_csv()

