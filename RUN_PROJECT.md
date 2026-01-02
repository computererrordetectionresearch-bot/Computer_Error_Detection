# 🚀 How to Run the Full Project

## Quick Start (Easiest Method)

### Option 1: Run Both Servers at Once
```powershell
cd "C:\Users\Pavindu Asinsala\Desktop\Recomendation Engine"
.\start-dev.bat
```

This will open two separate windows:
- **Backend Server** window (FastAPI on port 8000)
- **Frontend Server** window (Next.js on port 3000)

---

## Manual Start (Step by Step)

### Step 1: Start Backend (FastAPI)

Open **Terminal 1** (PowerShell or Command Prompt):

```powershell
# Navigate to backend directory
cd "C:\Users\Pavindu Asinsala\Desktop\Recomendation Engine\backend"

# Activate virtual environment
.\venv\Scripts\activate

# Start FastAPI server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

---

### Step 2: Start Frontend (Next.js)

Open **Terminal 2** (PowerShell or Command Prompt):

```powershell
# Navigate to frontend directory
cd "C:\Users\Pavindu Asinsala\Desktop\Recomendation Engine\frontend"

# Start Next.js development server
npm run dev
```

**Frontend will be available at:**
- Web App: http://localhost:3000

---

## Alternative: Using Individual Batch Files

### Start Backend Only:
```powershell
cd "C:\Users\Pavindu Asinsala\Desktop\Recomendation Engine\backend"
.\start-backend.bat
```

### Start Frontend Only:
```powershell
cd "C:\Users\Pavindu Asinsala\Desktop\Recomendation Engine"
.\start-frontend.bat
```

---

## Verify Everything is Running

1. **Backend Health Check:**
   - Visit: http://localhost:8000/docs
   - You should see the FastAPI Swagger documentation

2. **Frontend Check:**
   - Visit: http://localhost:3000
   - You should see the "Smart PC Assistant" homepage

3. **Test API Connection:**
   - The frontend should automatically connect to the backend
   - Try searching for a repair shop to verify the connection

---

## Troubleshooting

### Backend Issues:
- **Port 8000 already in use?**
  ```powershell
  # Kill process on port 8000 (Windows)
  netstat -ano | findstr :8000
  taskkill /PID <PID_NUMBER> /F
  ```

- **Virtual environment not activated?**
  ```powershell
  cd backend
  .\venv\Scripts\activate
  ```

- **Dependencies missing?**
  ```powershell
  cd backend
  .\venv\Scripts\activate
  pip install -r requirements.txt
  ```

### Frontend Issues:
- **Port 3000 already in use?**
  ```powershell
  # Kill process on port 3000 (Windows)
  netstat -ano | findstr :3000
  taskkill /PID <PID_NUMBER> /F
  ```

- **Node modules missing?**
  ```powershell
  cd frontend
  npm install
  ```

- **Build errors?**
  ```powershell
  cd frontend
  npm run build
  ```

---

## Stopping the Servers

- **Backend:** Press `Ctrl+C` in the backend terminal
- **Frontend:** Press `Ctrl+C` in the frontend terminal
- **Both:** Close the terminal windows

---

## Production Build (Optional)

### Build Frontend:
```powershell
cd frontend
npm run build
npm start
```

### Run Backend (Production):
```powershell
cd backend
.\venv\Scripts\activate
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 📝 Notes

- Backend runs on **port 8000**
- Frontend runs on **port 3000**
- Backend auto-reloads on code changes (--reload flag)
- Frontend uses Turbopack for faster development
- Make sure both servers are running before testing the full application

