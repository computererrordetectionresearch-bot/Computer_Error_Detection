"""
Master script to run the complete 100,000 error test and retraining workflow.
This script:
1. Creates 100,000 test errors (if not exists)
2. Tests error classification and hardware recommendation
3. Retrains models with corrections
"""

from pathlib import Path
import sys
import subprocess
import os

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

def run_script(script_name, description):
    """Run a Python script and handle errors."""
    print("\n" + "=" * 80)
    print(f"{description}")
    print("=" * 80)
    
    script_path = HERE / script_name
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        python_exe = get_python_executable()
        if python_exe != sys.executable:
            print(f"[INFO] Using virtual environment: {python_exe}")
        
        # Run the script
        result = subprocess.run(
            [python_exe, str(script_path)],
            cwd=str(HERE),
            capture_output=False,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def main():
    """Run the complete workflow."""
    print("=" * 80)
    print("100,000 ERROR TEST AND RETRAINING WORKFLOW")
    print("=" * 80)
    print("\nThis will:")
    print("1. Create 100,000 test error dataset")
    print("2. Test error classification accuracy")
    print("3. Test hardware recommendation accuracy")
    print("4. Retrain models with corrections")
    print("\nThis may take a while...")
    
    input("\nPress Enter to continue or Ctrl+C to cancel...")
    
    # Step 1: Create test dataset
    test_csv = DATA_DIR / "test_100000_errors.csv"
    if not test_csv.exists():
        success = run_script(
            "create_100000_test_errors.py",
            "Creating 100,000 test error dataset"
        )
        if not success:
            print("\n❌ Failed to create test dataset. Exiting.")
            return
    else:
        print(f"\n✅ Test dataset already exists: {test_csv}")
        print("   Skipping dataset creation. Delete the file to regenerate.")
    
    # Step 2: Run comprehensive tests
    success = run_script(
        "test_100000_errors_comprehensive.py",
        "Testing error classification and hardware recommendation on 100,000 errors"
    )
    if not success:
        print("\n⚠️  Tests completed with errors. Check the output above.")
        response = input("\nContinue with retraining anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Step 3: Retrain models
    success = run_script(
        "retrain_from_100000_test.py",
        "Retraining models with corrections from test results"
    )
    if not success:
        print("\n❌ Failed to retrain models. Check the errors above.")
        return
    
    print("\n" + "=" * 80)
    print("WORKFLOW COMPLETED")
    print("=" * 80)
    print("\n✅ All steps completed successfully!")
    print("\n⚠️  IMPORTANT: Restart the backend server to load the retrained models.")
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

