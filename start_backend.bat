@echo off
echo ========================================
echo Starting Error Detection Backend Server
echo ========================================
echo.

cd ml_backend

echo Checking if model exists...
if not exist "models\error_database_no_emb.pkl" (
    echo.
    echo ERROR: Model not found!
    echo Please run: python train_model.py
    echo.
    pause
    exit /b 1
)

echo.
echo Starting backend server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause





















