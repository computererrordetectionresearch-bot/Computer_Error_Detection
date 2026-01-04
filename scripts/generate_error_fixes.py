# FILE: scripts/generate_error_fixes.py
import csv
import os

# List of 50 commonly used apps
apps = [
    'Adobe Photoshop', 'Visual Studio Code', 'Node.js', 'Python', 'Chrome',
    'Firefox', 'Git', 'Docker', 'PostgreSQL', 'MongoDB', 'Microsoft Office',
    'Spotify', 'Discord', 'Zoom', 'Slack', 'WhatsApp', 'Telegram', 'VLC Media Player',
    'WinRAR', '7-Zip', 'Notepad++', 'Sublime Text', 'IntelliJ IDEA', 'Eclipse',
    'Android Studio', 'Xcode', 'MySQL', 'Redis', 'Elasticsearch', 'Kubernetes',
    'Terraform', 'Anaconda', 'Jupyter Notebook', 'TensorFlow', 'PyTorch',
    'Adobe Premiere Pro', 'Adobe Illustrator', 'Figma', 'Sketch', 'OBS Studio',
    'Steam', 'Epic Games Launcher', 'Adobe After Effects', 'Blender', 'Unity',
    'AutoCAD', 'SolidWorks', 'MATLAB', 'Tableau', 'Power BI'
]

# Common error patterns with fixes
error_patterns = [
    {
        'error': 'app is closing',
        'category': 'Application Crash / App Closing',
        'causes': {
            'Windows': 'Memory issues or corrupted preferences',
            'MacOS': 'Memory pressure or corrupted preferences'
        },
        'fixes': {
            'Windows': 'Close other applications to free memory || Reset application preferences || Update graphics drivers || Check for Windows updates || Reinstall application if issue persists',
            'MacOS': 'Free up RAM by closing other apps || Reset application preferences || Update macOS to latest version || Check Activity Monitor for memory issues || Reinstall application'
        }
    },
    {
        'error': 'installation failed',
        'category': 'Installation Failed',
        'causes': {
            'Windows': 'Insufficient disk space or corrupted installer',
            'MacOS': 'Insufficient disk space or permissions'
        },
        'fixes': {
            'Windows': 'Free up disk space (at least 10GB free) || Disable antivirus temporarily || Run installer as administrator || Check Windows compatibility || Download fresh installer',
            'MacOS': 'Free up disk space (at least 15GB) || Check disk permissions || Run Disk Utility first aid || Download fresh installer || Check macOS compatibility'
        }
    },
    {
        'error': 'missing dll',
        'category': 'Missing DLL / Library',
        'causes': {
            'Windows': 'Missing Visual C++ redistributables or system files',
            'MacOS': 'Missing system libraries or frameworks'
        },
        'fixes': {
            'Windows': 'Download and install Visual C++ Redistributable 2019 || Install all Windows updates || Run System File Checker (sfc /scannow) || Reinstall application || Check Windows Event Viewer for specific DLL',
            'MacOS': 'Install Xcode Command Line Tools: xcode-select --install || Update macOS to latest version || Reinstall application || Check Console.app for specific library errors'
        }
    },
    {
        'error': 'permission denied',
        'category': 'Permission Denied',
        'causes': {
            'Windows': 'User account lacks administrator rights',
            'MacOS': 'Insufficient permissions or security settings'
        },
        'fixes': {
            'Windows': 'Right-click installer and select Run as administrator || Add user to Administrators group || Disable User Account Control temporarily || Check folder permissions || Install to different location',
            'MacOS': 'Check System Preferences > Security & Privacy || Grant permissions when prompted || Run with sudo if needed || Check disk permissions || Install to Applications folder'
        }
    },
    {
        'error': 'license error',
        'category': 'License / Activation Error',
        'causes': {
            'Windows': 'Invalid or expired license key',
            'MacOS': 'Invalid or expired license key'
        },
        'fixes': {
            'Windows': 'Verify license key in account || Sign out and sign back in || Clear application cache files || Contact software support || Check subscription status',
            'MacOS': 'Verify license key in account || Sign out and sign back in || Clear application cache files || Contact software support || Check subscription status'
        }
    },
    {
        'error': 'network error',
        'category': 'Network / Update Error',
        'causes': {
            'Windows': 'Proxy or firewall blocking connection',
            'MacOS': 'Proxy or firewall blocking connection'
        },
        'fixes': {
            'Windows': 'Check internet connection || Configure proxy settings || Disable firewall temporarily || Check corporate network restrictions || Use offline installer',
            'MacOS': 'Check internet connection || Configure proxy settings in System Preferences || Disable firewall temporarily || Check corporate network restrictions || Use offline installer'
        }
    },
    {
        'error': 'update failed',
        'category': 'Network / Update Error',
        'causes': {
            'Windows': 'Update server unreachable or connection issues',
            'MacOS': 'Update server unreachable or connection issues'
        },
        'fixes': {
            'Windows': 'Check internet connection || Disable antivirus temporarily || Run updater as administrator || Manually download update || Check firewall settings',
            'MacOS': 'Check internet connection || Disable firewall temporarily || Run updater with admin rights || Manually download update || Check network settings'
        }
    },
    {
        'error': 'connection error',
        'category': 'Network / Update Error',
        'causes': {
            'Windows': 'Cannot connect to server or service',
            'MacOS': 'Cannot connect to server or service'
        },
        'fixes': {
            'Windows': 'Check internet connection || Verify server is online || Check firewall and proxy settings || Restart network adapter || Contact support if server issue',
            'MacOS': 'Check internet connection || Verify server is online || Check firewall and proxy settings || Restart network service || Contact support if server issue'
        }
    }
]

def generate_error_fixes():
    fixes = []
    fix_id = 1
    
    for app in apps:
        # Determine which OSes this app supports
        os_list = ['Windows 11', 'Windows 10']
        if app not in ['Notepad++', 'WinRAR', '7-Zip']:  # Most apps support MacOS
            os_list.append('MacOS')
        elif app == 'Xcode':
            os_list = ['MacOS']  # Xcode is MacOS only
        
        for os_name in os_list:
            os_type = 'Windows' if 'Windows' in os_name else 'MacOS'
            
            for pattern in error_patterns:
                fixes.append({
                    'id': fix_id,
                    'software': app,
                    'os': os_name,
                    'error_message': pattern['error'],
                    'probable_cause': pattern['causes'][os_type],
                    'fix_steps': pattern['fixes'][os_type]
                })
                fix_id += 1
    
    return fixes

if __name__ == '__main__':
    fixes = generate_error_fixes()
    
    # Write to CSV
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'error_fix_dataset.csv')
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'software', 'os', 'error_message', 'probable_cause', 'fix_steps'])
        writer.writeheader()
        writer.writerows(fixes)
    
    print(f'Generated {len(fixes)} error-fix entries for {len(apps)} applications')
    print(f'Saved to {csv_path}')

