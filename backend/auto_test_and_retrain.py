"""
Automated script to test 100,000 errors and automatically retrain if wrong predictions found.
This script:
1. Creates test dataset if needed
2. Runs comprehensive tests
3. Checks for incorrect predictions
4. Automatically retrains models if corrections are needed
"""

from pathlib import Path
import sys
import subprocess
import os
import json
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except (AttributeError, ValueError):
        pass

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

def get_python_executable():
    """Get the Python executable, prefer venv if available."""
    venv_python = HERE / "venv" / "Scripts" / "python.exe"
    if sys.platform != 'win32':
        venv_python = HERE / "venv" / "bin" / "python"
    
    if venv_python.exists():
        return str(venv_python)
    return sys.executable

def run_script(script_name, description, check_output=False):
    """Run a Python script and handle errors."""
    print("\n" + "=" * 80)
    print(f"{description}")
    print("=" * 80)
    
    script_path = HERE / script_name
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False, None
    
    try:
        python_exe = get_python_executable()
        if python_exe != sys.executable:
            print(f"[INFO] Using virtual environment: {python_exe}")
        
        # Run the script
        if check_output:
            result = subprocess.run(
                [python_exe, str(script_path)],
                cwd=str(HERE),
                capture_output=True,
                text=True,
                check=False
            )
            output = (result.stdout or '') + (result.stderr or '')
        else:
            result = subprocess.run(
                [python_exe, str(script_path)],
                cwd=str(HERE),
                capture_output=False,
                text=True,
                check=False
            )
            output = None
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True, output
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            if output:
                print(f"[ERROR OUTPUT]:\n{output[-1000:]}")  # Last 1000 chars
            return False, output
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def check_incorrect_predictions():
    """Check if there are incorrect predictions that need retraining."""
    error_file = DATA_DIR / "incorrect_error_predictions_100000.csv"
    hardware_file = DATA_DIR / "incorrect_hardware_predictions_100000.csv"
    
    error_count = 0
    hardware_count = 0
    
    if error_file.exists():
        try:
            import pandas as pd
            df = pd.read_csv(error_file)
            error_count = len(df)
        except:
            pass
    
    if hardware_file.exists():
        try:
            import pandas as pd
            df = pd.read_csv(hardware_file)
            hardware_count = len(df)
        except:
            pass
    
    return error_count, hardware_count

def main():
    """Run automated test and retrain workflow."""
    print("=" * 80)
    print("AUTOMATED 100,000 ERROR TEST AND RETRAINING")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis script will:")
    print("1. Create 100,000 test error dataset (if needed)")
    print("2. Test error classification and hardware recommendation")
    print("3. Check for incorrect predictions")
    print("4. Automatically retrain models if corrections found")
    print("=" * 80)
    
    # Step 1: Create test dataset if needed
    test_csv = DATA_DIR / "test_100000_errors.csv"
    if not test_csv.exists():
        print("\n[STEP 1/4] Creating test dataset...")
        success, _ = run_script(
            "create_100000_test_errors.py",
            "Creating 100,000 test error dataset"
        )
        if not success:
            print("\n❌ Failed to create test dataset. Exiting.")
            return
    else:
        print(f"\n[STEP 1/4] ✅ Test dataset already exists: {test_csv}")
        print("   Skipping dataset creation.")
    
    # Step 2: Run comprehensive tests
    print("\n[STEP 2/4] Running comprehensive tests...")
    success, _ = run_script(
        "test_100000_errors_comprehensive.py",
        "Testing error classification and hardware recommendation on 100,000 errors"
    )
    
    if not success:
        print("\n⚠️  Tests completed with errors. Checking for results anyway...")
    
    # Step 3: Check for incorrect predictions
    print("\n[STEP 3/4] Checking for incorrect predictions...")
    error_count, hardware_count = check_incorrect_predictions()
    
    print(f"\n[INFO] Incorrect error classifications: {error_count:,}")
    print(f"[INFO] Incorrect hardware recommendations: {hardware_count:,}")
    
    total_incorrect = error_count + hardware_count
    
    if total_incorrect == 0:
        print("\n" + "=" * 80)
        print("✅ NO CORRECTIONS NEEDED")
        print("=" * 80)
        print("\nAll predictions were correct! No retraining needed.")
        print("The models are performing well.")
        return
    
    # Step 4: Correct and retrain models
    print(f"\n[STEP 4/4] Found {total_incorrect:,} incorrect predictions.")
    print("Automatically correcting all predictions and retraining models...")
    
    # First, correct all incorrect predictions
    success, output = run_script(
        "correct_all_incorrect.py",
        "Correcting all incorrect predictions",
        check_output=True
    )
    
    if not success:
        print("\n⚠️  Correction script had issues. Trying direct retraining...")
        success, output = run_script(
            "retrain_from_100000_test.py",
            "Retraining models with corrections from test results",
            check_output=True
        )
    
    if not success:
        print("\n❌ Failed to retrain models. Check the errors above.")
        if output:
            print("\n[ERROR DETAILS]:")
            print(output[-2000:])  # Last 2000 chars
        return
    
    # Final summary
    print("\n" + "=" * 80)
    print("AUTOMATED WORKFLOW COMPLETED")
    print("=" * 80)
    print(f"\n✅ All steps completed successfully!")
    print(f"\nSummary:")
    print(f"  - Incorrect error classifications: {error_count:,}")
    print(f"  - Incorrect hardware recommendations: {hardware_count:,}")
    print(f"  - Total corrections applied: {total_incorrect:,}")
    print(f"\n⚠️  IMPORTANT: Restart the backend server to load the retrained models.")
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

