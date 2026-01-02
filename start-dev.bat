@echo off
echo Starting Shop Recommendation Engine Development Environment
echo.

echo Starting FastAPI Backend...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && uvicorn app:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Next.js Frontend...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting up...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause >nul
