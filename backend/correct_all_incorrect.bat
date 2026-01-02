@echo off
REM Automatically correct all incorrect predictions and retrain models

echo ================================================================================
echo Correcting All Incorrect Predictions and Retraining
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
echo [INFO] Correcting all incorrect predictions and retraining...
echo.

python correct_all_incorrect.py

echo.
echo ================================================================================
echo Process completed!
echo ================================================================================
pause

