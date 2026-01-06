@echo off
echo ========================================
echo Model Evaluation Script
echo ========================================
echo.

cd ml_backend

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing required packages if needed...
python -m pip install -q scikit-learn matplotlib seaborn

echo.
echo Running model evaluation...
echo.
python evaluate_model.py

if errorlevel 1 (
    echo.
    echo ERROR: Evaluation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Evaluation complete!
echo Charts saved to: ml_backend\charts\
echo ========================================
echo.
pause

