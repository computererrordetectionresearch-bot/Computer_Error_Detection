@echo off
echo ========================================
echo Starting Error Detection Frontend
echo ========================================
echo.

echo Checking dependencies...
if not exist "node_modules" (
    echo.
    echo Installing dependencies...
    call npm install
    echo.
)

echo.
echo Starting frontend server on http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

npm run dev

pause





















