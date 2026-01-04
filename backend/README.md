# FILE: backend/README.md
# Backend API Server

Separate Flask backend for the Installation Error Fixer models.

## Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

## Running the Backend

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### POST /api/detect
Detect error type and provide fixes or installation steps.

**Request:**
```json
{
  "text": "app is closing",
  "software": "Adobe Photoshop",
  "os": "Windows 11"
}
```

**Response:**
```json
{
  "type": "error",
  "category": "Application Crash / App Closing",
  "probable_cause": "...",
  "fix_steps": ["...", "..."],
  "fix_id": 1
}
```

### POST /api/feedback
Submit feedback about a fix.

**Request:**
```json
{
  "fix_id": 1,
  "success": true,
  "text": "app is closing",
  "software": "Adobe Photoshop",
  "os": "Windows 11"
}
```

### GET /health
Health check endpoint.

## Environment Variables

No environment variables required. The backend reads CSV files from the `data/` directory.

