#  PC Recommendation Engine

An intelligent system that helps users find repair shops, hardware products, and tools based on their computer issues using Machine Learning and Natural Language Processing.

##  Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Dependencies](#dependencies)
4. [Quick Start](#quick-start)
5. [Additional Documentation](#additional-documentation)

---

##  Overview

The **PC Recommendation Engine** is a full-stack intelligent system that provides personalized recommendations for:

- **Repair Shops** - Based on error type, location, budget, and urgency
- **Hardware Products** - Based on symptoms and needs
- **Tools & Software** - For DIY repairs and diagnostics

### Key Features

-  ML-powered shop ranking with explainable recommendations
-  NLP-based error type detection from free text
-  Hardware component recommendation with confidence scores
-  Product category classification
-  Multi-criteria filtering (location, budget, urgency)
-  Alternative recommendations for low-confidence predictions
-  Modern, responsive web interface
-  Hierarchical ML models for improved accuracy
-  Active learning loop with user feedback

### Technology Stack

- **Backend**: FastAPI (Python 3.13+)
- **Frontend**: Next.js 15.5.4 (React 19.1.0)
- **ML/AI**: Scikit-learn, TF-IDF Vectorization
- **Database**: Supabase (optional, falls back to CSV files)

---

##  Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Next.js)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Repairs    │  │   Products   │  │    Tools     │       │
│  │    Tab       │  │     Tab      │  │     Tab      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            │                                │
│                    ┌───────▼────────┐                       │
│                    │   API Client   │                       │
│                    │   (api.ts)     │                       │
│                    └───────┬────────┘                       │
└────────────────────────────┼────────────────────────────────┘
                             │ HTTP/REST
┌────────────────────────────▼───────────────────────────────┐
│                   BACKEND (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Endpoints Layer                     │  │
│  │  /rank_auto  /product_need_recommend  /detect_error  │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                               │
│  ┌─────────────────────────┼─────────────────────────────┐ │
│  │  Business Logic Layer   │                             │ │
│  │  - Feature Engineering  │                             │ │
│  │  - Rule-based Overrides │                             │ │
│  │  - Recommendation Logic │                             │ │
│  └─────────────────────────┼─────────────────────────────┘ │
│                            │                               │
│  ┌─────────────────────────┼────────────────────────────┐  │
│  │    ML Models Layer       │                           │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐              │  │
│  │  │  Shop    │ │  Error   │ │ Product  │              │  │
│  │  │ Ranking  │ │  Type    │ │  Need    │              │  │
│  │  │  Model   │ │   NLP    │ │   NLP    │              │  │
│  │  └──────────┘ └──────────┘ └──────────┘              │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                               │
│  ┌─────────────────────────┼────────────────────────────┐  │
│  │      Data Layer          │                           │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐              │  │
│  │  │ Supabase │ │   CSV    │ │  Models  │              │  │
│  │  │  (DB)    │ │  Files   │ │   (.pkl) │              │  │
│  │  └──────────┘ └──────────┘ └──────────┘              │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → Frontend collects user query (error description, filters)
2. **API Request** → Frontend sends HTTP request to FastAPI backend
3. **ML Processing** → Backend uses NLP models to classify/rank
4. **Business Logic** → Rule-based overrides and feature engineering applied
5. **Response** → Ranked recommendations with explanations returned
6. **Display** → Frontend renders results with confidence indicators

---

##  Dependencies

### Backend Dependencies

The backend requires Python 3.13+ and the following packages (see `backend/requirements.txt`):

```
fastapi>=0.104.0          # Web framework for building APIs
uvicorn[standard]>=0.24.0 # ASGI server for FastAPI
pydantic>=2.0.0           # Data validation using Python type annotations
pandas>=2.0.0             # Data manipulation and analysis
numpy>=1.24.0             # Numerical computing
scikit-learn==1.7.2       # Machine learning library
joblib>=1.3.0             # Model serialization and parallel processing
python-dotenv>=1.0.0      # Environment variable management
supabase>=2.0.0           # Supabase client (optional, for database)
```

**Install backend dependencies:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Frontend Dependencies

The frontend requires Node.js 18+ and npm/yarn. Key dependencies (see `frontend/package.json`):

**Runtime Dependencies:**
```json
{
  "next": "15.5.4",                    // React framework
  "react": "19.1.0",                   // UI library
  "react-dom": "19.1.0",               // React DOM renderer
  "@radix-ui/react-dialog": "^1.1.15", // Accessible dialog component
  "@radix-ui/react-select": "^2.2.6",  // Select component
  "@radix-ui/react-tabs": "^1.1.13",   // Tabs component
  "@radix-ui/react-toast": "^1.2.15",  // Toast notifications
  "framer-motion": "^12.23.22",        // Animation library
  "lucide-react": "^0.544.0",          // Icon library
  "tailwindcss": "^3.4.17",            // Utility-first CSS framework
  "typescript": "^5"                   // Type safety
}
```

**Dev Dependencies:**
```json
{
  "@types/node": "^20",
  "@types/react": "^19",
  "@types/react-dom": "^19",
  "eslint": "^9",
  "eslint-config-next": "15.5.4",
  "autoprefixer": "^10.4.21",
  "postcss": "^8.5.6"
}
```

**Install frontend dependencies:**
```bash
cd frontend
npm install
```

---

##  Quick Start

### Prerequisites

- Python 3.13+
- Node.js 18+
- npm or yarn
- Git (for cloning repository)

### Option 1: Quick Start (Both Servers)

Run both backend and frontend servers simultaneously:

```bash
.\start-dev.bat  # Windows
# or
.\start-dev.ps1  # PowerShell
```

This will start:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000

### Option 2: Manual Start

**1. Start Backend:**
```bash
cd backend
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**2. Start Frontend (in a new terminal):**
```bash
cd frontend
npm run dev
```

### Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc

### Verify Installation

1. Visit http://localhost:8000/docs to see FastAPI Swagger documentation
2. Visit http://localhost:3000 to see the web application
3. Try searching for a repair shop to test the connection

For detailed setup instructions, see [RUN_PROJECT.md](RUN_PROJECT.md).

---


##  Additional Documentation

For more detailed information, refer to:

- **[SYSTEM_DOCUMENTATION.md](SYSTEM_DOCUMENTATION.md)** - Complete system documentation including:
  - Detailed architecture overview
  - ML models description
  - API endpoints documentation
  - Frontend features
  - Data flow diagrams

- **[RUN_PROJECT.md](RUN_PROJECT.md)** - Step-by-step guide to run the project

- **[HARDWARE_RECOMMENDATION_IMPROVEMENTS.md](HARDWARE_RECOMMENDATION_IMPROVEMENTS.md)** - Hardware recommendation system improvements

- **Backend Documentation** (in `backend/` directory):
  - `API_DOCS.md` - API documentation
  - `COMPLETE_UPGRADE_GUIDE.md` - Upgrade guide
  - `ROBUST_MODEL_IMPLEMENTATION.md` - Model implementation details

---

##  System Requirements

### Backend
- **Python**: 3.13 or higher
- **RAM**: Minimum 4GB (8GB recommended for model training)
- **Storage**: 500MB+ for models and dependencies
- **OS**: Windows, macOS, or Linux

### Frontend
- **Node.js**: 18.0 or higher
- **npm**: 9.0 or higher (or yarn)
- **RAM**: 2GB+ recommended
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

---

##  ML Models

The system uses 4 trained ML models:

1. **Shop Ranking Model** (`reco_model.pkl`)
   - Type: Gradient Boosting Classifier
   - Purpose: Ranks repair shops based on multiple features
   - Accuracy: High (validated on shop data)

2. **Error Type NLP Model** (`nlp_error_model_error_type.pkl`)
   - Type: Multinomial Naive Bayes / SGDClassifier
   - Purpose: Classifies error type from free-text descriptions
   - Classes: 15 error types
   - Accuracy: ~87.5%

3. **Product Category NLP Model** (`nlp_error_model_product.pkl`)
   - Type: SGDClassifier
   - Purpose: Classifies product category from symptoms
   - Classes: 5 categories
   - Accuracy: 85.7%

4. **Product Need Model** (`product_need_model.pkl`)
   - Type: SGDClassifier with log_loss
   - Purpose: Recommends specific hardware components
   - Classes: 48 component types
   - Accuracy: 99.6%

For model training, see `backend/train_improved_models.py`.

---

## 📝 License

This project is part of a research initiative on computer error detection and recommendation systems.

---

## 👥 Contributors

- **Pavindu-Asinsala** - Main developer
- **computererrordetectionresearch-bot** - Repository maintainer

---

## 🔄 Version History

- **v2.0.0** (Current) - Production-ready version with hierarchical ML models
- **v1.0.0** - Initial release with basic recommendation functionality

---

**Status**: ✅ Production Ready  
**Last Updated**: 2026-01-02  
**Maintained by**: Project Team
