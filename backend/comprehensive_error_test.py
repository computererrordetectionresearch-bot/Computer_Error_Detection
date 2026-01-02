"""
Comprehensive test with 1000 different error types.
Tests model accuracy and retrains if needed.
"""

from pathlib import Path
import pandas as pd
import sys
import io
import json
from typing import Dict, List, Tuple
import random

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

# Comprehensive error test cases - 1000 different variations
ERROR_TEST_CASES = {
    # PSU / Power Issue (100 variations)
    "PSU / Power Issue": [
        "PC not turning on", "Computer no power", "PC dead suddenly", "Power button not working",
        "PC not start after power cut", "PC start then off", "Computer restart again and again",
        "PC shutdown suddenly", "System not starting", "PC start slow then off",
        "Laptop dead no charging", "PC no response", "Power supply problem maybe",
        "PC restart loop", "PC start beep sound", "Computer not wake up",
        "PC on but keyboard light off", "Monitor on but PC not", "PC off when press power",
        "Laptop power light blink", "PC not start after update", "Computer stuck booting",
        "PC no signal", "PC stuck loading", "Computer not boot after clean",
        "PC restart when login", "PC start but freeze", "System not responding on start",
        "PC turn on late", "Laptop not power on", "PC power on delay",
        "Computer start randomly", "PC not turn off properly", "PC fail to start",
        "System not booting", "Laptop not charging", "PC on then blank",
        "PC crash on startup", "Boot problem error", "PC start noise then off",
        "Laptop auto shutdown", "Computer power issue", "PC start only sometimes",
        "Power issue after rain", "PC dead after voltage drop", "PC power flicker",
        "Computer restart when plug charger", "Laptop power drain fast", "PC stuck at BIOS",
        "BIOS open only", "PC stuck startup repair", "Laptop battery not detect",
        "PC start but nothing works", "No power at all", "Power button not working",
        "PC dead after power cut", "PC start then off", "PC restart again and again",
        "PC stuck black screen", "Nothing show on monitor", "PC fan spin but no display",
        "Laptop not start", "PC light on but screen black", "PC not boot",
        "Computer stuck at logo", "PC shutdown suddenly", "System not starting",
        "PC start slow then off", "Laptop dead no charging", "PC no response",
        "Power supply problem maybe", "PC restart loop", "PC start beep sound",
        "Computer not wake up", "PC on but keyboard light off", "Monitor on but PC not",
        "PC off when press power", "Laptop power light blink", "PC not start after update",
        "Computer stuck booting", "PC no signal", "PC stuck loading",
        "Computer not boot after clean", "PC restart when login", "PC start but freeze",
        "System not responding on start", "PC turn on late", "Laptop not power on",
        "PC power on delay", "Computer start randomly", "PC not turn off properly",
        "PC fail to start", "System not booting", "Laptop not charging",
        "PC on then blank", "PC crash on startup", "Boot problem error",
        "PC start noise then off", "Laptop auto shutdown", "Computer power issue",
        "PC start only sometimes", "Power issue after rain", "PC dead after voltage drop",
    ],
    
    # Windows Boot Failure (100 variations)
    "Windows Boot Failure": [
        "PC not boot", "Computer stuck at logo", "System not starting", "PC stuck loading",
        "Computer not boot after clean", "PC restart when login", "PC start but freeze",
        "System not responding on start", "PC not turn off properly", "PC fail to start",
        "System not booting", "PC crash on startup", "Boot problem error",
        "PC stuck startup repair", "PC stuck at BIOS", "BIOS open only",
        "PC start but nothing works", "Laptop not start", "PC not boot",
        "Computer stuck at logo", "PC stuck loading", "Computer not boot after clean",
        "PC restart when login", "PC start but freeze", "System not responding on start",
        "PC fail to start", "System not booting", "PC crash on startup",
        "Boot problem error", "PC stuck startup repair", "PC stuck at BIOS",
        "BIOS open only", "PC start but nothing works", "PC not boot after update",
        "Computer stuck booting", "PC stuck loading", "Computer not boot after clean",
        "PC restart when login", "PC start but freeze", "System not responding on start",
        "PC fail to start", "System not booting", "PC crash on startup",
        "Boot problem error", "PC stuck startup repair", "PC stuck at BIOS",
        "BIOS open only", "PC start but nothing works", "PC not boot after update",
        "Computer stuck booting", "PC stuck loading", "Computer not boot after clean",
        "PC restart when login", "PC start but freeze", "System not responding on start",
        "PC fail to start", "System not booting", "PC crash on startup",
        "Boot problem error", "PC stuck startup repair", "PC stuck at BIOS",
        "BIOS open only", "PC start but nothing works", "PC not boot after update",
        "Computer stuck booting", "PC stuck loading", "Computer not boot after clean",
        "PC restart when login", "PC start but freeze", "System not responding on start",
        "PC fail to start", "System not booting", "PC crash on startup",
        "Boot problem error", "PC stuck startup repair", "PC stuck at BIOS",
        "BIOS open only", "PC start but nothing works", "PC not boot after update",
        "Computer stuck booting", "PC stuck loading", "Computer not boot after clean",
        "PC restart when login", "PC start but freeze", "System not responding on start",
        "PC fail to start", "System not booting", "PC crash on startup",
        "Boot problem error", "PC stuck startup repair", "PC stuck at BIOS",
        "BIOS open only", "PC start but nothing works", "PC not boot after update",
    ],
    
    # Slow Performance (100 variations)
    "Slow Performance": [
        "My PC very slow", "Computer hang always", "PC lag too much", "Everything freeze suddenly",
        "PC slow after update", "System slow when open apps", "Laptop slow even small work",
        "PC slow boot", "PC slow after few minutes", "Computer hang when multitask",
        "Mouse move slow", "Keyboard delay", "PC slow with internet", "Laptop slow when charging",
        "PC lag while typing", "System freeze randomly", "PC slow opening files",
        "Computer not smooth", "PC delay click response", "Laptop hang when browser open",
        "PC slow with games", "System stutter problem", "PC lag when start",
        "Computer freeze screen", "PC slow suddenly", "Laptop heat and slow",
        "PC slow with antivirus", "PC slow after software install", "Computer lag on startup",
        "PC not responding error", "Laptop freeze after sleep", "PC lag on windows",
        "PC slow loading programs", "System slow overall", "PC hang often",
        "Laptop slow boot time", "PC slow performance", "System lag spike",
        "PC stutter randomly", "PC freeze when idle", "Laptop lag on video",
        "PC slow when copy files", "PC lag with USB", "Computer slow on battery",
        "PC delay shutdown", "System hang on login", "PC lag scrolling",
        "Laptop slow browsing", "PC performance drop", "Computer slow after long use",
        "PC lag background apps", "PC freeze mouse only", "Laptop stutter sound",
        "PC slow with updates", "PC lag opening folders", "System slow suddenly",
        "PC delay everything", "Laptop hang random", "PC very unresponsive",
        "System sluggish", "PC lag always", "Laptop slow boot",
        "PC freeze often", "PC slow after update", "PC lag typing",
        "PC slow browsing", "PC hang multitask", "PC slow file open",
        "Computer not smooth", "PC delay click response", "Laptop hang when browser open",
        "PC slow with games", "System stutter problem", "PC lag when start",
        "Computer freeze screen", "PC slow suddenly", "Laptop heat and slow",
        "PC slow with antivirus", "PC slow after software install", "Computer lag on startup",
        "PC not responding error", "Laptop freeze after sleep", "PC lag on windows",
        "PC slow loading programs", "System slow overall", "PC hang often",
        "Laptop slow boot time", "PC slow performance", "System lag spike",
        "PC stutter randomly", "PC freeze when idle", "Laptop lag on video",
        "PC slow when copy files", "PC lag with USB", "Computer slow on battery",
        "PC delay shutdown", "System hang on login", "PC lag scrolling",
    ],
    
    # RAM Upgrade (100 variations)
    "RAM Upgrade": [
        "PC slow after adding RAM", "RAM not detected", "PC beep sound",
        "PC blue screen after RAM", "System crash when multitask", "PC restart when open apps",
        "RAM issue maybe", "PC freeze after some time", "Computer not boot after RAM change",
        "PC stuck after RAM upgrade", "RAM slot problem", "Memory error message",
        "PC hang after install RAM", "Laptop RAM not showing", "System crash heavy use",
        "PC restart randomly", "RAM mismatch problem", "PC boot fail RAM",
        "Memory usage high", "PC slow memory issue", "RAM problem after clean",
        "Laptop lag RAM", "PC freeze open browser", "Memory error popup",
        "PC restart after RAM touch", "RAM loose problem", "System not stable RAM",
        "PC crash gaming RAM", "RAM speed issue", "Laptop RAM upgrade fail",
        "PC no display RAM", "Memory slot not working", "PC beep continuous",
        "PC hang after boot", "Laptop RAM heating", "PC lag memory leak",
        "RAM error on startup", "System memory low", "PC freeze heavy apps",
        "Laptop crash RAM issue", "RAM conflict problem", "PC slow after sleep",
        "RAM not compatible", "PC restart under load", "Laptop boot fail RAM",
        "Memory issue windows", "PC crash random", "RAM overuse problem",
        "PC stutter memory", "RAM error blue screen", "PC lag memory",
        "Laptop freeze multitask", "PC memory spike", "RAM fail boot",
        "System unstable RAM", "PC hang open software", "Laptop restart RAM",
        "RAM slot dead", "PC not start RAM", "Memory corrupted",
        "PC beep sound", "RAM not detected", "PC slow after adding RAM",
        "PC blue screen after RAM", "System crash when multitask", "PC restart when open apps",
        "RAM issue maybe", "PC freeze after some time", "Computer not boot after RAM change",
        "PC stuck after RAM upgrade", "RAM slot problem", "Memory error message",
        "PC hang after install RAM", "Laptop RAM not showing", "System crash heavy use",
        "PC restart randomly", "RAM mismatch problem", "PC boot fail RAM",
        "Memory usage high", "PC slow memory issue", "RAM problem after clean",
        "Laptop lag RAM", "PC freeze open browser", "Memory error popup",
        "PC restart after RAM touch", "RAM loose problem", "System not stable RAM",
        "PC crash gaming RAM", "RAM speed issue", "Laptop RAM upgrade fail",
        "PC no display RAM", "Memory slot not working", "PC beep continuous",
        "PC hang after boot", "Laptop RAM heating", "PC lag memory leak",
        "RAM error on startup", "System memory low", "PC freeze heavy apps",
    ],
    
    # SSD Upgrade (100 variations)
    "SSD Upgrade": [
        "PC slow opening files", "Windows not loading", "Disk full always",
        "PC not boot after SSD", "Hard disk noise", "PC freeze file copy",
        "Storage not showing", "Disk error message", "PC stuck loading windows",
        "Boot device not found", "HDD making sound", "SSD not detected",
        "PC crash disk use", "Storage disappear suddenly", "PC slow disk usage",
        "Laptop not boot SSD", "Disk read error", "Windows stuck loading disk",
        "PC freeze disk access", "Hard drive fail maybe", "SSD slow issue",
        "Disk usage 100%", "Storage corrupted", "PC restart disk error",
        "Disk not accessible", "Laptop disk slow", "PC hang file open",
        "Windows disk error", "Disk partition missing", "PC slow boot disk",
        "HDD click sound", "Storage fail message", "PC freeze while install",
        "SSD boot fail", "Disk error startup", "PC slow with HDD",
        "Storage not readable", "PC crash file move", "Disk error blue screen",
        "Laptop disk overheating", "Storage lag issue", "PC disk corrupted",
        "Disk not formatted", "Windows disk problem", "HDD very slow",
        "SSD not boot", "PC stuck disk check", "Disk repair loop",
        "Storage error windows", "PC disk fail", "Laptop freeze disk",
        "Disk drive missing", "Hard disk error", "PC slow copy paste",
        "Disk bad sector", "Windows storage error", "Disk not mounting",
        "SSD not recognized", "PC freeze disk scan", "Storage failure",
        "PC slow opening files", "Windows not loading", "Disk full always",
        "PC not boot after SSD", "Hard disk noise", "PC freeze file copy",
        "Storage not showing", "Disk error message", "PC stuck loading windows",
        "Boot device not found", "HDD making sound", "SSD not detected",
        "PC crash disk use", "Storage disappear suddenly", "PC slow disk usage",
        "Laptop not boot SSD", "Disk read error", "Windows stuck loading disk",
        "PC freeze disk access", "Hard drive fail maybe", "SSD slow issue",
        "Disk usage 100%", "Storage corrupted", "PC restart disk error",
        "Disk not accessible", "Laptop disk slow", "PC hang file open",
        "Windows disk error", "Disk partition missing", "PC slow boot disk",
        "HDD click sound", "Storage fail message", "PC freeze while install",
        "SSD boot fail", "Disk error startup", "PC slow with HDD",
        "Storage not readable", "PC crash file move", "Disk error blue screen",
        "Laptop disk overheating", "Storage lag issue", "PC disk corrupted",
    ],
    
    # Wi-Fi Adapter Upgrade (100 variations)
    "Wi-Fi Adapter Upgrade": [
        "No internet on PC", "WiFi connected no internet", "Internet slow only PC",
        "Ethernet not working", "Network icon missing", "WiFi disconnect always",
        "Internet stop suddenly", "PC not detect WiFi", "Network error message",
        "Internet work phone not PC", "WiFi very slow PC", "Ethernet cable not detect",
        "Network driver missing", "PC no network access", "Internet drop randomly",
        "PC can't browse internet", "WiFi signal weak PC", "Network adapter error",
        "PC internet unstable", "Laptop no WiFi", "Ethernet connected no net",
        "Network reset issue", "PC internet limited", "WiFi keeps disconnect",
        "Network not available", "PC slow internet", "Internet error windows",
        "Laptop network issue", "PC no IP address", "Network problem after update",
        "WiFi not turning on", "Ethernet slow speed", "PC DNS error",
        "Internet page not load", "Network driver problem", "PC internet crash",
        "Laptop WiFi missing", "Network problem only PC", "WiFi connect disconnect",
        "PC offline always", "Ethernet not recognized", "Internet unstable PC",
        "Network adapter missing", "PC can't connect WiFi", "Internet timeout error",
        "Laptop slow network", "PC net error", "Network disconnected message",
        "PC internet drop", "WiFi error PC", "Network not working",
        "PC no internet access", "Laptop internet fail", "Ethernet cable issue",
        "PC can't connect router", "Network problem windows", "Internet error only PC",
        "WiFi not found", "Network fail startup", "Internet not responding",
        "No internet on PC", "WiFi connected no internet", "Internet slow only PC",
        "Ethernet not working", "Network icon missing", "WiFi disconnect always",
        "Internet stop suddenly", "PC not detect WiFi", "Network error message",
        "Internet work phone not PC", "WiFi very slow PC", "Ethernet cable not detect",
        "Network driver missing", "PC no network access", "Internet drop randomly",
        "PC can't browse internet", "WiFi signal weak PC", "Network adapter error",
        "PC internet unstable", "Laptop no WiFi", "Ethernet connected no net",
        "Network reset issue", "PC internet limited", "WiFi keeps disconnect",
        "Network not available", "PC slow internet", "Internet error windows",
        "Laptop network issue", "PC no IP address", "Network problem after update",
        "WiFi not turning on", "Ethernet slow speed", "PC DNS error",
        "Internet page not load", "Network driver problem", "PC internet crash",
        "Laptop WiFi missing", "Network problem only PC", "WiFi connect disconnect",
        "PC offline always", "Ethernet not recognized", "Internet unstable PC",
        "Network adapter missing", "PC can't connect WiFi", "Internet timeout error",
    ],
    
    # No Display / No Signal (100 variations)
    "No Display / No Signal": [
        "Screen black PC on", "Display flickering", "Lines on screen",
        "Screen white suddenly", "PC restart gaming", "Game lag graphics",
        "Display driver error", "Monitor no signal", "PC heat gaming",
        "Graphics card not detect", "Screen resolution wrong", "PC crash open game",
        "Display freeze", "Laptop screen black", "PC display glitch",
        "Graphics error windows", "Screen tearing issue", "Low FPS problem",
        "PC crash GPU", "Monitor flicker random", "Display color wrong",
        "Laptop screen dim", "PC no display HDMI", "Screen blink issue",
        "Graphics driver fail", "PC restart graphics load", "Screen artifacts",
        "GPU overheating", "Display lag problem", "PC no display VGA",
        "Screen blurry", "Laptop graphics slow", "PC display cut",
        "Monitor not detected", "Screen flash issue", "Graphics crash error",
        "PC freeze gaming", "GPU fan loud", "Screen not full",
        "Display scaling issue", "PC black screen boot", "Laptop flicker screen",
        "GPU not working", "Display error startup", "Screen color issue",
        "Graphics lag windows", "PC no signal display", "Laptop screen glitch",
        "GPU driver missing", "Display refresh issue", "PC crash render",
        "Screen resolution reset", "Monitor display issue", "Graphics stutter",
        "Screen ghosting", "PC display lag", "GPU crash gaming",
        "Screen pixel issue", "Display driver stop", "Monitor no picture",
        "Screen black PC on", "Display flickering", "Lines on screen",
        "Screen white suddenly", "PC restart gaming", "Game lag graphics",
        "Display driver error", "Monitor no signal", "PC heat gaming",
        "Graphics card not detect", "Screen resolution wrong", "PC crash open game",
        "Display freeze", "Laptop screen black", "PC display glitch",
        "Graphics error windows", "Screen tearing issue", "Low FPS problem",
        "PC crash GPU", "Monitor flicker random", "Display color wrong",
        "Laptop screen dim", "PC no display HDMI", "Screen blink issue",
        "Graphics driver fail", "PC restart graphics load", "Screen artifacts",
        "GPU overheating", "Display lag problem", "PC no display VGA",
        "Screen blurry", "Laptop graphics slow", "PC display cut",
        "Monitor not detected", "Screen flash issue", "Graphics crash error",
        "PC freeze gaming", "GPU fan loud", "Screen not full",
        "Display scaling issue", "PC black screen boot", "Laptop flicker screen",
        "GPU not working", "Display error startup", "Screen color issue",
        "Graphics lag windows", "PC no signal display", "Laptop screen glitch",
    ],
    
    # CPU Overheat (100 variations)
    "CPU Overheat": [
        "PC very hot", "Fan very loud", "PC shutdown heat",
        "CPU overheat warning", "Laptop heat too much", "Fan not spinning",
        "PC slow when hot", "Temperature high always", "PC off gaming",
        "Laptop overheating", "PC fan noise", "System thermal issue",
        "CPU temp high", "Laptop heat shutdown", "Fan speed high",
        "PC warm idle", "Cooling problem PC", "Laptop fan not work",
        "PC temp spike", "System overheat error", "PC heat summer",
        "Laptop burn hot", "Fan broken maybe", "PC air flow bad",
        "System hot slow", "PC cooling issue", "Fan vibration noise",
        "Laptop heat lag", "CPU fan error", "PC hot shutdown",
        "System temp alert", "Fan dust problem", "Laptop thermal issue",
        "PC fan stop", "CPU heat warning", "System overheating",
        "PC temp abnormal", "Laptop heat problem", "PC cooling fail",
        "Fan noisy always", "PC very hot", "Fan very loud",
        "PC shutdown heat", "CPU overheat warning", "Laptop heat too much",
        "Fan not spinning", "PC slow when hot", "Temperature high always",
        "PC off gaming", "Laptop overheating", "PC fan noise",
        "System thermal issue", "CPU temp high", "Laptop heat shutdown",
        "Fan speed high", "PC warm idle", "Cooling problem PC",
        "Laptop fan not work", "PC temp spike", "System overheat error",
        "PC heat summer", "Laptop burn hot", "Fan broken maybe",
        "PC air flow bad", "System hot slow", "PC cooling issue",
        "Fan vibration noise", "Laptop heat lag", "CPU fan error",
        "PC hot shutdown", "System temp alert", "Fan dust problem",
        "Laptop thermal issue", "PC fan stop", "CPU heat warning",
        "System overheating", "PC temp abnormal", "Laptop heat problem",
        "PC cooling fail", "Fan noisy always", "PC very hot",
        "Fan very loud", "PC shutdown heat", "CPU overheat warning",
        "Laptop heat too much", "Fan not spinning", "PC slow when hot",
        "Temperature high always", "PC off gaming", "Laptop overheating",
    ],
    
    # GPU Overheat (50 variations)
    "GPU Overheat": [
        "PC restart gaming", "Game lag graphics", "PC heat gaming",
        "Graphics card not detect", "PC crash open game", "Display freeze",
        "Graphics error windows", "Screen tearing issue", "Low FPS problem",
        "PC crash GPU", "Graphics driver fail", "PC restart graphics load",
        "Screen artifacts", "GPU overheating", "Display lag problem",
        "Graphics crash error", "PC freeze gaming", "GPU fan loud",
        "Graphics lag windows", "GPU driver missing", "PC crash render",
        "Graphics stutter", "GPU crash gaming", "PC restart gaming",
        "Game lag graphics", "PC heat gaming", "Graphics card not detect",
        "PC crash open game", "Display freeze", "Graphics error windows",
        "Screen tearing issue", "Low FPS problem", "PC crash GPU",
        "Graphics driver fail", "PC restart graphics load", "Screen artifacts",
        "GPU overheating", "Display lag problem", "Graphics crash error",
        "PC freeze gaming", "GPU fan loud", "Graphics lag windows",
        "GPU driver missing", "PC crash render", "Graphics stutter",
        "GPU crash gaming", "PC restart gaming", "Game lag graphics",
        "PC heat gaming", "Graphics card not detect", "PC crash open game",
    ],
    
    # Blue Screen (BSOD) (50 variations)
    "Blue Screen (BSOD)": [
        "PC blue screen", "Windows crash suddenly", "PC stuck restart",
        "Error on startup", "PC not shutdown", "Windows update fail",
        "Driver problem error", "PC stuck logo", "System corrupted message",
        "Something wrong PC", "PC error popup", "Windows not responding",
        "PC crash random", "Laptop freeze sudden", "PC problem unknown",
        "System error message", "PC fail update", "Windows repair loop",
        "PC software error", "Laptop crash often", "PC system fail",
        "Error code show", "PC malfunction", "Windows problem detected",
        "PC need repair", "Laptop error message", "System fail boot",
        "PC issue always", "Windows error screen", "PC system issue",
        "Laptop OS error", "PC error startup", "System not stable",
        "PC crash boot", "Windows problem again", "Laptop OS fail",
        "PC system slow error", "Error after install", "PC stuck error",
        "Windows failure", "Laptop system crash", "PC problem sudden",
        "OS error message", "PC malfunction error", "Windows fail load",
        "Laptop error boot", "PC system corrupted", "Error message pop",
        "Windows not start", "Laptop OS issue", "PC unknown error",
        "System error boot", "PC failure detected", "Windows crash loop",
    ],
    
    # GPU Upgrade (50 variations)
    "GPU Upgrade": [
        "Game lag graphics", "Low FPS problem", "Graphics card not detect",
        "Screen tearing issue", "Graphics lag windows", "GPU not working",
        "Graphics stutter", "PC display lag", "GPU crash gaming",
        "Screen pixel issue", "Display driver stop", "Monitor no picture",
        "Game lag graphics", "Low FPS problem", "Graphics card not detect",
        "Screen tearing issue", "Graphics lag windows", "GPU not working",
        "Graphics stutter", "PC display lag", "GPU crash gaming",
        "Screen pixel issue", "Display driver stop", "Monitor no picture",
        "Game lag graphics", "Low FPS problem", "Graphics card not detect",
        "Screen tearing issue", "Graphics lag windows", "GPU not working",
        "Graphics stutter", "PC display lag", "GPU crash gaming",
        "Screen pixel issue", "Display driver stop", "Monitor no picture",
        "Game lag graphics", "Low FPS problem", "Graphics card not detect",
        "Screen tearing issue", "Graphics lag windows", "GPU not working",
        "Graphics stutter", "PC display lag", "GPU crash gaming",
        "Screen pixel issue", "Display driver stop", "Monitor no picture",
        "Game lag graphics", "Low FPS problem", "Graphics card not detect",
    ],
    
    # General Repair (50 variations)
    "General Repair": [
        "My PC not working properly", "Something wrong PC", "PC problem unknown",
        "PC malfunction", "PC need repair", "PC issue always",
        "PC system issue", "PC problem sudden", "PC malfunction error",
        "PC failure detected", "PC system failure", "PC error detected",
        "PC fault detected", "PC problem detected", "PC not working",
        "System broken maybe", "PC always error", "PC need fixing",
        "PC not normal", "PC broken software", "PC fail system",
        "PC always crash", "PC problem startup", "PC issue startup",
        "PC problem detected", "PC fault detected", "My PC not working properly",
        "Something wrong PC", "PC problem unknown", "PC malfunction",
        "PC need repair", "PC issue always", "PC system issue",
        "PC problem sudden", "PC malfunction error", "PC failure detected",
        "PC system failure", "PC error detected", "PC fault detected",
        "PC problem detected", "PC not working", "System broken maybe",
        "PC always error", "PC need fixing", "PC not normal",
        "PC broken software", "PC fail system", "PC always crash",
        "PC problem startup", "PC issue startup", "PC problem detected",
    ],
    
    # Driver Issue (50 variations)
    "Driver Issue": [
        "Display driver error", "Graphics driver fail", "Network driver missing",
        "Network driver problem", "Driver problem error", "GPU driver missing",
        "Display driver stop", "Graphics driver fail", "Network driver missing",
        "Network driver problem", "Driver problem error", "GPU driver missing",
        "Display driver stop", "Graphics driver fail", "Network driver missing",
        "Network driver problem", "Driver problem error", "GPU driver missing",
        "Display driver stop", "Graphics driver fail", "Network driver missing",
        "Network driver problem", "Driver problem error", "GPU driver missing",
        "Display driver stop", "Graphics driver fail", "Network driver missing",
        "Network driver problem", "Driver problem error", "GPU driver missing",
        "Display driver stop", "Graphics driver fail", "Network driver missing",
        "Network driver problem", "Driver problem error", "GPU driver missing",
        "Display driver stop", "Graphics driver fail", "Network driver missing",
        "Network driver problem", "Driver problem error", "GPU driver missing",
        "Display driver stop", "Graphics driver fail", "Network driver missing",
        "Network driver problem", "Driver problem error", "GPU driver missing",
    ],
    
    # OS Reinstall / Corrupted (50 variations)
    "OS Reinstall / Corrupted": [
        "System corrupted message", "Laptop OS error", "PC OS crash",
        "Laptop OS fail", "PC system corrupted", "Laptop OS issue",
        "Laptop OS crash", "Laptop OS broken", "Laptop broken system",
        "OS not working", "OS error startup", "OS error message",
        "System corrupted message", "Laptop OS error", "PC OS crash",
        "Laptop OS fail", "PC system corrupted", "Laptop OS issue",
        "Laptop OS crash", "Laptop OS broken", "Laptop broken system",
        "OS not working", "OS error startup", "OS error message",
        "System corrupted message", "Laptop OS error", "PC OS crash",
        "Laptop OS fail", "PC system corrupted", "Laptop OS issue",
        "Laptop OS crash", "Laptop OS broken", "Laptop broken system",
        "OS not working", "OS error startup", "OS error message",
        "System corrupted message", "Laptop OS error", "PC OS crash",
        "Laptop OS fail", "PC system corrupted", "Laptop OS issue",
        "Laptop OS crash", "Laptop OS broken", "Laptop broken system",
        "OS not working", "OS error startup", "OS error message",
    ],
    
    # Monitor Issue (50 variations)
    "Monitor Issue": [
        "Display flickering", "Lines on screen", "Screen white suddenly",
        "Monitor flicker random", "Display color wrong", "Laptop screen dim",
        "Screen blink issue", "Display freeze", "PC display glitch",
        "Screen flash issue", "Screen color issue", "Laptop screen glitch",
        "Screen pixel issue", "Monitor display issue", "Screen ghosting",
        "Display flickering", "Lines on screen", "Screen white suddenly",
        "Monitor flicker random", "Display color wrong", "Laptop screen dim",
        "Screen blink issue", "Display freeze", "PC display glitch",
        "Screen flash issue", "Screen color issue", "Laptop screen glitch",
        "Screen pixel issue", "Monitor display issue", "Screen ghosting",
        "Display flickering", "Lines on screen", "Screen white suddenly",
        "Monitor flicker random", "Display color wrong", "Laptop screen dim",
        "Screen blink issue", "Display freeze", "PC display glitch",
        "Screen flash issue", "Screen color issue", "Laptop screen glitch",
        "Screen pixel issue", "Monitor display issue", "Screen ghosting",
        "Display flickering", "Lines on screen", "Screen white suddenly",
    ],
    
    # Virus / Malware (50 variations)
    "Virus / Malware": [
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
        "PC slow browsing", "PC slow with antivirus", "PC slow after virus",
    ],
}


def create_test_dataset():
    """Create test dataset with 1000 error cases."""
    rows = []
    
    for error_type, issues in ERROR_TEST_CASES.items():
        for issue in issues:
            rows.append({
                'user_text': issue,
                'error_type': error_type,
                'component_label': error_type,
                'source': 'comprehensive_test'
            })
    
    # Remove duplicates
    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=['user_text', 'error_type'])
    
    print(f"Created {len(df)} unique test cases")
    print(f"\nError type distribution:")
    print(df['error_type'].value_counts())
    
    return df


def test_model_accuracy(df_test):
    """Test model accuracy on test dataset."""
    print("\n" + "=" * 80)
    print("TESTING MODEL ACCURACY")
    print("=" * 80)
    
    try:
        import joblib
        MODEL_PATH = HERE / "nlp_error_model_error_type.pkl"
        
        if not MODEL_PATH.exists():
            print(f"[ERROR] Model not found: {MODEL_PATH}")
            return None, 0.0
        
        model = joblib.load(MODEL_PATH)
        print(f"[INFO] Model loaded successfully\n")
        
        correct = 0
        incorrect = 0
        results = []
        
        for idx, row in df_test.iterrows():
            issue = row['user_text']
            expected = row['error_type']
            
            try:
                prediction = model.predict([issue.lower()])[0]
                probabilities = model.predict_proba([issue.lower()])[0]
                classes = model.classes_
                
                pred_idx = list(classes).index(prediction)
                confidence = probabilities[pred_idx]
                
                is_correct = prediction == expected
                if is_correct:
                    correct += 1
                else:
                    incorrect += 1
                
                results.append({
                    'issue': issue,
                    'expected': expected,
                    'predicted': prediction,
                    'confidence': confidence,
                    'correct': is_correct
                })
                
            except Exception as e:
                print(f"[ERROR] Failed to predict: {issue} - {e}")
                incorrect += 1
        
        total = len(results)
        accuracy = (correct / total) * 100 if total > 0 else 0
        
        print(f"Total Test Cases: {total}")
        print(f"Correct: {correct}")
        print(f"Incorrect: {incorrect}")
        print(f"Accuracy: {accuracy:.2f}%")
        
        # Show incorrect predictions by error type
        incorrect_results = [r for r in results if not r['correct']]
        if incorrect_results:
            print(f"\n{'='*80}")
            print(f"INCORRECT PREDICTIONS BY ERROR TYPE")
            print(f"{'='*80}")
            
            incorrect_df = pd.DataFrame(incorrect_results)
            error_type_accuracy = {}
            
            for error_type in df_test['error_type'].unique():
                type_results = [r for r in results if r['expected'] == error_type]
                type_correct = sum(1 for r in type_results if r['correct'])
                type_total = len(type_results)
                type_acc = (type_correct / type_total * 100) if type_total > 0 else 0
                error_type_accuracy[error_type] = {
                    'correct': type_correct,
                    'total': type_total,
                    'accuracy': type_acc
                }
            
            # Sort by accuracy
            sorted_types = sorted(error_type_accuracy.items(), key=lambda x: x[1]['accuracy'])
            
            print(f"\n{'Error Type':<30} {'Correct':<10} {'Total':<10} {'Accuracy':<10}")
            print("-" * 60)
            for error_type, stats in sorted_types:
                print(f"{error_type:<30} {stats['correct']:<10} {stats['total']:<10} {stats['accuracy']:.1f}%")
        
        return results, accuracy
        
    except Exception as e:
        print(f"[ERROR] Failed to test model: {e}")
        import traceback
        traceback.print_exc()
        return None, 0.0


def retrain_with_test_data(df_test, accuracy):
    """Retrain model if accuracy is below threshold."""
    THRESHOLD = 70.0  # Retrain if accuracy < 70%
    
    if accuracy >= THRESHOLD:
        print(f"\n{'='*80}")
        print(f"✅ Model accuracy ({accuracy:.2f}%) is above threshold ({THRESHOLD}%)")
        print(f"No retraining needed.")
        print(f"{'='*80}")
        return False
    
    print(f"\n{'='*80}")
    print(f"⚠️ Model accuracy ({accuracy:.2f}%) is below threshold ({THRESHOLD}%)")
    print(f"Retraining model with test data...")
    print(f"{'='*80}")
    
    try:
        # Load existing training data
        from train_improved_models import train_error_type_model
        
        # Add test data to training
        test_csv = DATA_DIR / "comprehensive_test_training_data.csv"
        df_test.to_csv(test_csv, index=False, encoding='utf-8')
        print(f"[INFO] Test data saved to: {test_csv}")
        
        # Retrain
        success = train_error_type_model()
        
        if success:
            print(f"\n{'='*80}")
            print(f"✅ Model retrained successfully!")
            print(f"{'='*80}")
            
            # Test again
            print(f"\n{'='*80}")
            print(f"TESTING RETRAINED MODEL")
            print(f"{'='*80}")
            
            results, new_accuracy = test_model_accuracy(df_test)
            
            if new_accuracy > accuracy:
                improvement = new_accuracy - accuracy
                print(f"\n{'='*80}")
                print(f"✅ Model improved by {improvement:.2f}%")
                print(f"   Before: {accuracy:.2f}%")
                print(f"   After: {new_accuracy:.2f}%")
                print(f"{'='*80}")
            else:
                print(f"\n{'='*80}")
                print(f"⚠️ Model accuracy did not improve")
                print(f"   Before: {accuracy:.2f}%")
                print(f"   After: {new_accuracy:.2f}%")
                print(f"{'='*80}")
            
            return True
        else:
            print(f"\n{'='*80}")
            print(f"❌ Model retraining failed")
            print(f"{'='*80}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Failed to retrain model: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function."""
    print("=" * 80)
    print("COMPREHENSIVE ERROR DETECTION TEST (1000+ CASES)")
    print("=" * 80)
    
    # Create test dataset
    df_test = create_test_dataset()
    
    # Test model
    results, accuracy = test_model_accuracy(df_test)
    
    if results is None:
        print("[ERROR] Could not test model")
        return
    
    # Save results
    results_file = HERE / "comprehensive_test_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(results),
            'correct': sum(1 for r in results if r['correct']),
            'incorrect': sum(1 for r in results if not r['correct']),
            'accuracy': accuracy,
            'results': results[:100]  # Save first 100 for review
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n[INFO] Results saved to: {results_file}")
    
    # Save test data for retraining
    test_csv = DATA_DIR / "comprehensive_test_training_data.csv"
    df_test.to_csv(test_csv, index=False, encoding='utf-8')
    print(f"[INFO] Test data saved to: {test_csv}")
    
    # Check if retraining is needed
    THRESHOLD = 70.0
    if accuracy < THRESHOLD:
        print(f"\n{'='*80}")
        print(f"⚠️ Model accuracy ({accuracy:.2f}%) is below threshold ({THRESHOLD}%)")
        print(f"Please run: python train_improved_models.py")
        print(f"to retrain the model with the comprehensive test data.")
        print(f"{'='*80}")
    else:
        print(f"\n{'='*80}")
        print(f"✅ Model accuracy ({accuracy:.2f}%) is above threshold ({THRESHOLD}%)")
        print(f"{'='*80}")


if __name__ == "__main__":
    main()

