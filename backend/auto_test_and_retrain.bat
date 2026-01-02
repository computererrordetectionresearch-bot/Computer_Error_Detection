@echo off
REM Automated script to test 100,000 errors and retrain if wrong predictions found

echo ================================================================================
echo Automated 100,000 Error Test and Retraining
echo ================================================================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please create a virtual environment first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment and run script
call venv\Scripts\activate.bat

echo [INFO] Virtual environment activated
echo [INFO] Running automated test and retrain...
echo.

python auto_test_and_retrain.py

echo.
echo ================================================================================
echo Process completed!
echo ================================================================================
pause

