@echo off
REM Run 100,000 error tests with virtual environment activated

echo ================================================================================
echo Running 100,000 Error Test with Virtual Environment
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

REM Activate virtual environment and run test
call venv\Scripts\activate.bat

echo [INFO] Virtual environment activated
echo [INFO] Running comprehensive test...
echo.

python test_100000_errors_comprehensive.py

echo.
echo ================================================================================
echo Test completed!
echo ================================================================================
pause

