# FILE: models/get_install_steps.py
import pandas as pd
import sys
import os
import json

def load_installation_steps():
    """Load installation steps from CSV"""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'installation_steps.csv')
    df = pd.read_csv(csv_path)
    return df

def get_installation_steps(software, os_name):
    """Get installation steps for software and OS"""
    df = load_installation_steps()
    
    normalized_software = software.strip().lower()
    normalized_os = os_name.strip().lower()
    
    match = df[
        (df['software'].str.lower() == normalized_software) &
        (df['os'].str.lower() == normalized_os)
    ]
    
    if match.empty:
        return None
    
    steps_str = match.iloc[0]['installation_steps']
    steps = [step.strip() for step in steps_str.split(' || ') if step.strip()]
    return steps

if __name__ == '__main__':
    # Command line interface
    if len(sys.argv) < 3:
        print("Usage: python get_install_steps.py <software> <os>")
        sys.exit(1)
    
    software = sys.argv[1]
    os_name = sys.argv[2]
    result = get_installation_steps(software, os_name)
    
    if result:
        print(json.dumps(result))
    else:
        print("null")

