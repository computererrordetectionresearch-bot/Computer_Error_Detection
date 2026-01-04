@echo off
echo ========================================
echo Retraining Error Detection Model
echo ========================================
echo.

echo Step 1: Stopping backend server (if running)...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 2: Training model with new data...
cd ml_backend
python train_model.py

echo.
echo Step 3: Model training complete!
echo.
echo Next: Restart the backend server using start_backend.bat
pause

















