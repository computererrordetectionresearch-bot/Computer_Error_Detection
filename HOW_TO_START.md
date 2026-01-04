# How to Start the Application

## Quick Start Guide

### Prerequisites
- Python 3.8+ installed
- Node.js 18+ and npm installed
- All dependencies installed (see below if not done)

---

## Step 1: Install Dependencies (First Time Only)

### Install Python Dependencies
```bash
cd ml_backend
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install fastapi uvicorn pandas numpy scikit-learn sentence-transformers torch python-multipart
```

### Install Frontend Dependencies
```bash
npm install
```

---

## Step 2: Train the Model (First Time Only)

**Important**: You must train the model before starting the backend!

```bash
cd ml_backend
python train_model.py
```

This will:
- Load all CSV datasets from the `Datasets` folder
- Create semantic embeddings
- Save the model to `ml_backend/models/`

**Note**: First run takes 5-10 minutes (downloads ~80MB model)

---

## Step 3: Start the Backend Server

### Option A: Using Python directly
```bash
cd ml_backend
python app.py
```

### Option B: Using uvicorn
```bash
cd ml_backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Backend will run on**: `http://localhost:8000`

**Wait for**: "Model loaded successfully!" message

---

## Step 4: Start the Frontend Server

Open a **NEW terminal window** and run:

```bash
npm run dev
```

**Frontend will run on**: `http://localhost:3000`

**Wait for**: "Ready" message in the terminal

---

## Step 5: Open in Browser

Open your browser and navigate to:
```
http://localhost:3000
```

---

## Using Batch Files (Windows)

### Start Backend
Double-click: `start_backend.bat`

### Start Frontend
Double-click: `start_frontend.bat` (in a new window)

---

## Troubleshooting

### Backend Issues

**"Model not found" error:**
- Make sure you ran `python train_model.py` first
- Check that `ml_backend/models/` folder exists

**Port 8000 already in use:**
- Stop any process using port 8000
- Or change port in `app.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`

**Python packages missing:**
```bash
pip install fastapi uvicorn pandas numpy scikit-learn sentence-transformers torch
```

### Frontend Issues

**Port 3000 already in use:**
```bash
npm run dev -- -p 3001
```

**Dependencies missing:**
```bash
npm install
```

**Build errors:**
```bash
rm -rf .next node_modules
npm install
npm run dev
```

### Connection Issues

**"Failed to connect to ML backend":**
- Make sure backend is running on port 8000
- Check backend terminal for errors
- Verify backend health: Open `http://localhost:8000/health` in browser

---

## Verification

### Check Backend
Open in browser: `http://localhost:8000/health`

Should return:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "database_size": 1329
}
```

### Check Frontend
Open in browser: `http://localhost:3000`

Should show the AI Error Detection interface

---

## Stopping Servers

### Backend
- Press `Ctrl+C` in the backend terminal
- Or close the terminal window

### Frontend
- Press `Ctrl+C` in the frontend terminal
- Or close the terminal window

---

## Quick Reference

| Component | Command | Port | URL |
|-----------|---------|------|-----|
| Backend | `cd ml_backend && python app.py` | 8000 | http://localhost:8000 |
| Frontend | `npm run dev` | 3000 | http://localhost:3000 |
| Health Check | - | 8000 | http://localhost:8000/health |

---

## Development Mode

Both servers support hot-reload:
- **Backend**: Use `uvicorn app:app --reload`
- **Frontend**: `npm run dev` (auto-reloads on file changes)

---

## Production Build

### Build Frontend
```bash
npm run build
npm start
```

### Backend (Production)
```bash
cd ml_backend
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Need Help?

1. Check that both servers are running
2. Verify ports 3000 and 8000 are not in use
3. Check terminal windows for error messages
4. Ensure model files exist in `ml_backend/models/`





















