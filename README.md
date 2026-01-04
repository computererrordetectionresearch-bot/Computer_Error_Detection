# Installation Error Fixer

A comprehensive web application that provides intelligent installation guides and error resolution for software across multiple operating systems. The system uses machine learning models to classify errors and match them with appropriate fixes.

## Overview

This project is an AI-powered installation and error-fixing assistant that helps users:
- **Get step-by-step installation guides** for various software applications
- **Diagnose and fix installation errors** using ML-based classification and matching
- **Learn from user feedback** to improve accuracy over time

The system intelligently distinguishes between installation requests and error reports, routing each to the appropriate handler with specialized ML models.

### Key Features

- 🎯 **Intelligent Error Classification**: Automatically categorizes errors into 20+ categories
- 🔍 **Smart Error-Fix Matching**: Uses TF-IDF and n-gram similarity to find the best solutions
- 📚 **Comprehensive Installation Guides**: Step-by-step instructions for 50+ software applications
- 🎓 **Learning System**: Incorporates user feedback to improve fix recommendations
- 🌐 **Multi-Platform Support**: Windows 11, Windows 10, and macOS
- 🚀 **Modern Stack**: Next.js frontend with Flask backend

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REQUEST                              │
│  "I want to install X" OR "X has error Y"                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Error Detection     │
         │  (is_error_request)  │
         └───────┬───────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌──────────────┐   ┌──────────────┐
│ INSTALLATION│   │ ERROR FIX    │
│   STEPS     │   │   HANDLER    │
└──────────────┘   └──────────────┘
        │                 │
        ▼                 ▼
┌──────────────┐   ┌──────────────┐
│ installation │   │ error        │
│_steps.csv    │   │_fix_dataset  │
│              │   │.csv          │
└──────────────┘   └──────────────┘
        │                 │
        ▼                 ▼
┌──────────────┐   ┌──────────────┐
│ Direct       │   │ ML Matching  │
│ Lookup      │   │ + Feedback   │
└──────────────┘   └──────────────┘
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Home Page  │  │ Installation │  │  Error Fix   │     │
│  │              │  │    Page      │  │    Page      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                        │ HTTP/REST API
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (Flask)                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │  API Endpoints:                                    │    │
│  │  • /api/installation/steps                        │    │
│  │  • /api/error/classify                            │    │
│  │  • /api/error/fix                                 │    │
│  │  • /api/detect (unified)                         │    │
│  │  • /api/feedback                                  │    │
│  └────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Models     │ │    Data      │ │  Feedback    │
│  Directory   │ │  Directory   │ │   System     │
│              │ │              │ │              │
│ • classify_  │ │ • install_   │ │ • feedback.  │
│   error.py   │ │   steps.csv  │ │   csv        │
│ • match_     │ │ • error_fix_  │ │              │
│   error_fix  │ │   dataset.csv│ │              │
│   .py        │ │ • error_      │ │              │
│ • get_       │ │   category.csv│ │              │
│   install_   │ │              │ │              │
│   steps.py   │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
```

### Data Flow

#### Installation Request Flow
1. User submits: "I want to install Adobe Photoshop"
2. Frontend → `/api/detect` or `/api/installation/steps`
3. Backend detects: NOT an error → Installation handler
4. Model: `get_installation_steps("Adobe Photoshop", "Windows 11")`
5. Data: Lookup in `installation_steps.csv`
6. Response: Installation steps array

#### Error Request Flow
1. User submits: "app is closing"
2. Frontend → `/api/detect` or `/api/error/fix`
3. Backend detects: IS an error → Error handler
4. Model 1: `classify_error("app is closing")` → Category
5. Model 2: `match_error_fix(text, software, os, category)` → Best fix
6. Data: Match from `error_fix_dataset.csv`
7. Response: Error category + Fix steps + Fix ID

## Dependencies

### Frontend Dependencies

**Production Dependencies:**
- `next@14.0.4` - React framework for production
- `react@^18.2.0` - UI library
- `react-dom@^18.2.0` - React DOM renderer
- `@supabase/supabase-js@^2.39.0` - Supabase client
- `natural@^6.10.3` - Natural language processing
- `csv-parse@^5.5.3` - CSV parsing
- `csv-stringify@^6.4.4` - CSV stringification

**Development Dependencies:**
- `typescript@^5.3.3` - TypeScript compiler
- `@types/node@^20.10.6` - Node.js type definitions
- `@types/react@^18.2.46` - React type definitions
- `@types/react-dom@^18.2.18` - React DOM type definitions
- `eslint@^8.56.0` - Linting tool
- `eslint-config-next@14.0.4` - Next.js ESLint config
- `tsx@^4.21.0` - TypeScript execution

### Backend Dependencies

**Python Requirements (`backend/requirements.txt`):**
- `flask==3.0.0` - Web framework
- `flask-cors==4.0.0` - CORS support
- `pandas>=2.2.0` - Data manipulation
- `scikit-learn>=1.5.0` - Machine learning library
- `numpy>=1.26.0` - Numerical computing

**Model Dependencies (`models/requirements.txt`):**
- `pandas>=2.2.0` - Data processing
- `scikit-learn>=1.5.0` - ML algorithms (TF-IDF, cosine similarity)
- `numpy>=1.26.0` - Numerical operations

### System Requirements

- **Node.js**: v18.0.0 or higher
- **Python**: 3.8 or higher
- **Operating Systems**: Windows 10/11, macOS, Linux

## Installation & Setup

### Prerequisites

1. Install Node.js and npm
2. Install Python 3.8+
3. Install pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Installation
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

4. **Install model dependencies**
   ```bash
   cd models
   pip install -r requirements.txt
   cd ..
   ```

5. **Train the models** (first time setup)
   ```bash
   npm run train
   # or
   python models/train_models.py
   ```

6. **Start the backend server**
   ```bash
   cd backend
   python app.py
   # Server runs on http://localhost:5001
   ```

7. **Start the frontend server** (in a new terminal)
   ```bash
   npm run dev
   # Frontend runs on http://localhost:3000
   ```

## API Endpoints

### Installation Endpoints

- `POST /api/installation/steps` - Get installation steps for software/OS
- `GET /api/installation/list` - List all available software

### Error Endpoints

- `POST /api/error/classify` - Classify error text into category
- `POST /api/error/fix` - Get fix steps for an error
- `GET /api/error/list` - List all error categories

### Unified Endpoint

- `POST /api/detect` - Auto-detect installation vs error request

### Feedback Endpoint

- `POST /api/feedback` - Submit feedback about a fix

For detailed API documentation, see `backend/API_DOCUMENTATION.md`.

## Project Structure

```
Installation/
├── app/                    # Next.js frontend application
│   ├── api/                # API routes
│   ├── installation/       # Installation page
│   ├── error-fix/          # Error fix page
│   └── page.tsx            # Home page
├── backend/                # Flask backend
│   ├── app.py              # Main Flask application
│   └── requirements.txt    # Backend dependencies
├── models/                 # ML models
│   ├── classify_error.py   # Error classification model
│   ├── match_error_fix.py  # Error-fix matching model
│   ├── get_install_steps.py # Installation steps model
│   ├── train_models.py     # Model training script
│   └── requirements.txt    # Model dependencies
├── data/                   # Data files
│   ├── installation_steps.csv
│   ├── error_fix_dataset.csv
│   ├── error_category.csv
│   └── feedback.csv
├── scripts/                 # Utility scripts
├── styles/                  # CSS styles
└── tests/                   # Test files
```

## Project History

### Commit History

The project has evolved through multiple iterations with contributions from various team members:

**Recent Commits:**
- `36ddda8` - venuja, 7 minutes ago: Initial commit - Computer Error Detection Project
- `2d50a4b` - Pavindu-Asinsala, 4 hours ago: new
- `ff7bd12` - Udana07, 4 hours ago: update
- `292961b` - Pavindu-Asinsala, 5 hours ago: commit
- `33b9d10` - Pavindu-Asinsala, 5 hours ago: readme
- `ffc6e24` - Pavindu-Asinsala, 5 hours ago: Readme
- `ba178c4` - Udana07, 11 hours ago: update the README.md file
- `3a21afd` - Udana07, 11 hours ago: Initial project upload
- `8f58465` - Udana07, 14 hours ago: Remove ignored files from repository
- `76b788c` - Udana07, 14 hours ago: Remove ignored files from repository
- `b27690b` - Udana07, 14 hours ago: Update .gitignore: ignore docs and batch scripts, keep Datasets
- `aba294c` - Udana07, 15 hours ago: Initial project upload
- `014b70d` - Pavindu-Asinsala, 2 days ago: commit
- `a00ae45` - Pavindu-Asinsala, 2 days ago: Merge branch 'Recommendation-Engine'
- `ee6d5d6` - Pavindu-Asinsala, 2 days ago: Initial commit: Recommendation Engine project
- `c4cf772` - computererrordetectionresearch-bot, 2 days ago: Update README.md
- `86b740c` - computererrordetectionresearch-bot, 2 days ago: Initial commit

### Development Timeline

1. **Initial Project Setup** (2 days ago)
   - Created repository structure
   - Set up basic Next.js frontend
   - Implemented Flask backend skeleton

2. **Core Features Development** (1-2 days ago)
   - Implemented error classification model
   - Created error-fix matching algorithm
   - Added installation steps lookup

3. **Data Integration** (14-15 hours ago)
   - Added CSV data files
   - Implemented data loading functions
   - Created feedback system

4. **UI/UX Improvements** (11 hours ago)
   - Enhanced frontend pages
   - Improved error display formatting
   - Added structured solution steps

5. **Model Improvements** (Recent)
   - Enhanced NLP preprocessing
   - Improved TF-IDF algorithms
   - Expanded error categories (13 → 20+)
   - Added 22+ new error-fix mappings

6. **System Refinement** (Recent)
   - Fixed CSV parsing issues
   - Improved port management
   - Enhanced error handling
   - Updated documentation

### Key Milestones

- ✅ **Error Classification System**: Implemented ML-based error categorization
- ✅ **Error-Fix Matching**: Created intelligent matching algorithm using TF-IDF
- ✅ **Installation Guides**: Added support for 50+ software applications
- ✅ **Feedback Learning**: Implemented user feedback system for continuous improvement
- ✅ **Multi-Platform Support**: Windows 11, Windows 10, macOS
- ✅ **20+ Error Categories**: Comprehensive error classification
- ✅ **1200+ Error-Fix Mappings**: Extensive database of solutions

## Usage

### Getting Installation Steps

1. Navigate to the Installation page
2. Select software and operating system
3. Click "Get Installation Steps"
4. Follow the step-by-step guide

### Fixing Errors

1. Navigate to the Error Fix page
2. Enter error description
3. Select software and operating system
4. Click "Get Fix"
5. Follow the provided solution steps
6. Provide feedback on whether the fix worked

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Specify your license here]

## Contact

For questions or support, please open an issue in the repository.

---

**Last Updated**: 2024
**Version**: 1.0.0
