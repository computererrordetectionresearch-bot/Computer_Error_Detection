# 🖥️ PC Recommendation Engine - Complete System Documentation

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Machine Learning Models](#machine-learning-models)
4. [API Endpoints](#api-endpoints)
5. [Frontend Features](#frontend-features)
6. [Data Flow](#data-flow)
7. [Technologies Used](#technologies-used)
8. [File Structure](#file-structure)
9. [Setup & Deployment](#setup--deployment)

---

## 🎯 System Overview

The **PC Recommendation Engine** is an intelligent system that helps users find:
- **Repair Shops** - Based on error type, location, budget, and urgency
- **Hardware Products** - Based on symptoms and needs
- **Tools & Software** - For DIY repairs and diagnostics

The system uses **Machine Learning** and **Natural Language Processing** to understand user queries and provide personalized recommendations with explainable reasoning.

### Key Features
- ✅ ML-powered shop ranking with explainable recommendations
- ✅ NLP-based error type detection from free text
- ✅ Hardware component recommendation with confidence scores
- ✅ Product category classification
- ✅ Multi-criteria filtering (location, budget, urgency)
- ✅ Alternative recommendations for low-confidence predictions
- ✅ Modern, responsive web interface

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Next.js)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Repairs    │  │   Products   │  │    Tools     │     │
│  │    Tab       │  │     Tab      │  │     Tab      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            │                                │
│                    ┌───────▼────────┐                       │
│                    │   API Client   │                       │
│                    │   (api.ts)     │                       │
│                    └───────┬────────┘                       │
└────────────────────────────┼─────────────────────────────────┘
                             │ HTTP/REST
┌────────────────────────────▼─────────────────────────────────┐
│                   BACKEND (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Endpoints Layer                      │   │
│  │  /rank_auto  /product_need_recommend  /detect_error   │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌─────────────────────────┼─────────────────────────────┐ │
│  │  Business Logic Layer   │                             │ │
│  │  - Feature Engineering  │                             │ │
│  │  - Rule-based Overrides │                             │ │
│  │  - Recommendation Logic │                             │ │
│  └─────────────────────────┼─────────────────────────────┘ │
│                            │                                 │
│  ┌─────────────────────────┼─────────────────────────────┐ │
│  │    ML Models Layer       │                             │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │ │
│  │  │  Shop    │ │  Error   │ │ Product   │            │ │
│  │  │ Ranking  │ │  Type    │ │  Need     │            │ │
│  │  │  Model   │ │   NLP    │ │   NLP     │            │ │
│  │  └──────────┘ └──────────┘ └──────────┘            │ │
│  └──────────────────────────────────────────────────────┘ │
│                            │                                 │
│  ┌─────────────────────────┼─────────────────────────────┐ │
│  │      Data Layer          │                             │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │ │
│  │  │ Supabase │ │   CSV    │ │  Models   │            │ │
│  │  │  (DB)    │ │  Files   │ │   (.pkl)  │            │ │
│  │  └──────────┘ └──────────┘ └──────────┘            │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 Machine Learning Models

### 1. Shop Recommendation Model (`reco_model.pkl`)
- **Type**: Gradient Boosting Classifier
- **Purpose**: Ranks repair shops based on multiple features
- **Input Features**:
  - Shop ratings, reviews, verification status
  - District match, error type match
  - Budget fit, urgency penalty
  - Quality score (calculated)
- **Output**: Binary classification (recommended/not recommended) with probability scores
- **Accuracy**: Tested and validated on shop data
- **Training Data**: Shop features with user preferences

### 2. Error Type NLP Model (`nlp_error_model_error_type.pkl`)
- **Type**: Multinomial Naive Bayes / SGDClassifier
- **Purpose**: Classifies error type from free-text descriptions
- **Input**: User's error description (text)
- **Output**: Error type label + confidence score
- **Classes**: 15 error types
  - GPU Overheat, CPU Overheat, Blue Screen (BSOD)
  - SSD Upgrade, RAM Upgrade, GPU Upgrade
  - PSU / Power Issue, Wi-Fi Adapter Upgrade
  - Monitor or GPU Check, No Display / No Signal
  - Windows Boot Failure, Slow Performance
  - Phone Connection Issue, USB / Port Issue
  - General Repair
- **Training Data**: 224 samples from `error_texts.csv`
- **Test Accuracy**: ~87.5% (7/8 test cases correct)
- **Features**: TF-IDF vectorization with n-grams (1-3)

### 3. Product Category NLP Model (`nlp_error_model_product.pkl`)
- **Type**: SGDClassifier with log_loss
- **Purpose**: Classifies product category from symptoms
- **Input**: User's symptom description (text)
- **Output**: Product category + confidence score
- **Classes**: 5 categories
  - GPU, SSD, RAM, PSU, Wi-Fi Adapter
- **Training Data**: 92 samples (14 primary + 78 augmented from hardware dataset)
- **Test Accuracy**: 85.7% (6/7 test cases correct)
- **Features**: TF-IDF vectorization with n-grams (1-2)

### 4. Product Need Model (`product_need_model.pkl`)
- **Type**: SGDClassifier with log_loss
- **Purpose**: Recommends specific hardware components from user needs
- **Input**: User's problem description (text)
- **Output**: Component label + confidence score + top 5 alternatives
- **Classes**: 48 component types
  - RAM Upgrade, SSD Upgrade, GPU Upgrade
  - CPU Fan Replacement, CPU Cooler Upgrade
  - WiFi Adapter Upgrade, PSU Upgrade
  - Monitor or GPU Check, Thermal Paste Reapply
  - And 38 more component types
- **Training Data**: 9,722 samples from `hardware_component_dataset_merged.csv`
- **Test Accuracy**: 99.6% (excellent performance)
- **Features**: TF-IDF vectorization with n-grams (1-2)
- **Special Features**:
  - Confidence thresholds (High ≥0.7, Medium 0.4-0.7, Low <0.4)
  - Always returns top 5 alternatives
  - Rule-based overrides for common patterns

### Model Training
- **Training Script**: `backend/train_improved_models.py`
- **Testing Script**: `backend/test_all_models.py`
- **Algorithm Selection**: Automatically tests multiple algorithms and selects best based on cross-validation

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000
```

### Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### 1. **GET /** - Root
Get API information and status.

#### 2. **POST /rank_auto** - Shop Recommendations
Get ranked shop recommendations with explainable reasons.

**Request:**
```json
{
  "error_type": "GPU Overheat",
  "budget": "medium",
  "urgency": "high",
  "user_district": "Colombo",
  "top_k": 10
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "shop_id": "shop_123",
      "shop_name": "TechFix Colombo",
      "score": 0.95,
      "reason": "We recommend because...",
      "factors": ["Specialization match", "Location", "High rating"],
      "avg_rating": 4.5,
      "reviews": 150,
      "verified": true
    }
  ]
}
```

#### 3. **POST /product_need_recommend** - Hardware Recommendation
Get hardware component recommendation with confidence scores and alternatives.

**Request:**
```json
{
  "text": "My computer is running very slowly",
  "budget": "medium",
  "district": "Colombo"
}
```

**Response:**
```json
{
  "component": "RAM Upgrade",
  "confidence": 0.865,
  "definition": "RAM (Random Access Memory)...",
  "why_useful": "More RAM helps...",
  "extra_explanation": "Based on your description...",
  "alternatives": [
    {"label": "RAM Upgrade", "confidence": 0.865},
    {"label": "SSD Upgrade", "confidence": 0.082}
  ],
  "is_low_confidence": false
}
```

#### 4. **POST /nlp/detect_error_type** - Error Type Detection
Detect error type from free-text description.

**Request:**
```json
{
  "text": "My PC keeps showing blue screen"
}
```

**Response:**
```json
{
  "label": "Blue Screen (BSOD)",
  "confidence": 0.85,
  "source": "ml",
  "alternatives": [...]
}
```

#### 5. **POST /nlp/detect_product_category** - Product Category Detection
Detect product category from symptoms.

**Request:**
```json
{
  "text": "Low FPS in games"
}
```

**Response:**
```json
{
  "label": "GPU",
  "confidence": 0.96,
  "source": "ml",
  "alternatives": [...]
}
```

#### 6. **POST /rank_products_auto** - Product Recommendations
Get product recommendations based on error type and filters.

#### 7. **GET /tools_recommend** - Tool Recommendations
Get recommended tools and software for specific error types.

#### 8. **POST /full_recommendation** - Complete Recommendation
Get shops, products, and tools in one request.

#### 9. **POST /feedback** - Submit Feedback
Submit user feedback for model improvement.

#### 10. **GET /health/supabase** - Health Check
Check Supabase connection status.

---

## 🎨 Frontend Features

### Technology Stack
- **Framework**: Next.js 15.5.4 (React 19.1.0)
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **State Management**: React Hooks (useState, useEffect)

### Main Features

#### 1. **Repairs Tab**
- Search for repair shops by error type
- Filter by district, budget, urgency
- View shop details with ratings, reviews, turnaround time
- Compare multiple shops side-by-side
- Get explainable recommendations with reasons

#### 2. **Products Tab**
- Hardware component recommendations
- Product category suggestions
- Filter by budget and district
- View product details and specifications
- See alternative recommendations

#### 3. **Tools Tab**
- Recommended tools and software
- Filter by OS, license type
- View tool descriptions and download links
- See why each tool is recommended

#### 4. **Smart Features**
- **Error Suggestions**: Auto-suggestions as you type
- **Voice Input**: Speech-to-text for queries (optional)
- **Confidence Indicators**: Visual indicators for ML confidence
- **Alternative Options**: Always shows alternatives for low-confidence predictions
- **Responsive Design**: Works on desktop, tablet, and mobile

### Components Structure
```
frontend/src/
├── app/
│   ├── page.tsx          # Main page with tabs
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/
│   ├── ShopCard.tsx      # Shop recommendation card
│   ├── ProductCard.tsx   # Product recommendation card
│   ├── ToolCard.tsx      # Tool recommendation card
│   ├── QueryBar.tsx      # Search input component
│   ├── ErrorSuggestions.tsx  # Auto-suggestions
│   ├── FeedbackModal.tsx     # Feedback form
│   └── ui/               # Reusable UI components
├── lib/
│   ├── api.ts            # API client functions
│   ├── detect.ts         # Error detection utilities
│   └── productNeedApi.ts # Product need API
└── types/
    ├── index.ts          # TypeScript types
    └── recommend.ts     # Recommendation types
```

---

## 🔄 Data Flow

### Shop Recommendation Flow
```
User Input (Error Type, District, Budget)
    ↓
[Frontend] → POST /rank_auto
    ↓
[Backend] → Fetch Shops (Supabase/CSV)
    ↓
[Backend] → Build Features (ratings, matches, etc.)
    ↓
[ML Model] → Rank Shops (reco_model.pkl)
    ↓
[Backend] → Generate Explanations
    ↓
[Frontend] → Display Ranked Results
```

### Hardware Recommendation Flow
```
User Input (Free Text: "My PC is slow")
    ↓
[Frontend] → POST /product_need_recommend
    ↓
[Backend] → NLP Model (product_need_model.pkl)
    ↓
[Backend] → Get Top 5 Predictions + Confidence
    ↓
[Backend] → Apply Rule-based Overrides
    ↓
[Backend] → Lookup Component Info
    ↓
[Backend] → Determine Confidence Level
    ↓
[Frontend] → Display Primary + Alternatives
```

### Error Detection Flow
```
User Input (Free Text: "Blue screen error")
    ↓
[Frontend] → POST /nlp/detect_error_type
    ↓
[Backend] → Check Priority Rules
    ↓
[Backend] → NLP Model (nlp_error_model_error_type.pkl)
    ↓
[Backend] → Fallback Keyword Matching
    ↓
[Frontend] → Display Error Type + Confidence
```

---

## 🛠️ Technologies Used

### Backend
- **Python 3.13**
- **FastAPI** - Web framework
- **Scikit-learn** - Machine learning
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Joblib** - Model serialization
- **Pydantic** - Data validation
- **Supabase** - Database (optional, falls back to CSV)
- **Uvicorn** - ASGI server

### Frontend
- **Next.js 15.5.4** - React framework
- **React 19.1.0** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Radix UI** - Accessible components
- **Framer Motion** - Animations
- **Lucide React** - Icons

### ML/AI
- **Scikit-learn** - ML algorithms
- **TF-IDF Vectorization** - Text preprocessing
- **Logistic Regression** - Classification
- **SGDClassifier** - Stochastic gradient descent
- **Multinomial Naive Bayes** - Text classification
- **Gradient Boosting** - Shop ranking

---

## 📁 File Structure

```
Recomendation Engine/
├── backend/
│   ├── app.py                    # Main FastAPI application
│   ├── reco_model.pkl            # Shop ranking model
│   ├── nlp_error_model_error_type.pkl  # Error type NLP model
│   ├── nlp_error_model_product.pkl     # Product category NLP model
│   ├── product_need_model.pkl          # Hardware recommendation model
│   ├── reco_features.json        # Feature configuration
│   ├── train_improved_models.py  # Model training script
│   ├── test_all_models.py        # Model testing script
│   ├── test_hardware_recommendation.py  # Hardware recommendation tests
│   ├── API_DOCS.md               # API documentation
│   ├── start-backend.bat          # Backend startup script
│   └── venv/                      # Python virtual environment
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx          # Main page
│   │   │   ├── layout.tsx        # Root layout
│   │   │   └── globals.css       # Global styles
│   │   ├── components/           # React components
│   │   ├── lib/                  # API clients
│   │   └── types/                # TypeScript types
│   ├── package.json              # Dependencies
│   └── next.config.ts            # Next.js config
│
├── data/
│   ├── shops.csv                 # Shop data
│   ├── products.csv              # Product data
│   ├── error_texts.csv           # Error type training data
│   ├── product_texts.csv         # Product category training data
│   ├── hardware_component_dataset_merged.csv  # Hardware training data
│   └── feedback.csv                # User feedback
│
├── start-dev.bat                 # Start both servers
├── start-frontend.bat             # Start frontend only
├── RUN_PROJECT.md                 # How to run guide
├── SYSTEM_DOCUMENTATION.md        # This file
└── HARDWARE_RECOMMENDATION_IMPROVEMENTS.md  # Hardware system docs
```

---

## 🚀 Setup & Deployment

### Prerequisites
- Python 3.13+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python train_improved_models.py  # Train models
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Quick Start (Both Servers)
```bash
.\start-dev.bat
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📊 System Statistics

### Models
- **Total Models**: 4 ML models
- **Total Training Samples**: ~10,000+
- **Model Accuracy**: 85-99.6% depending on model
- **Model Size**: ~5-50 MB per model

### Data
- **Shops**: Variable (from Supabase/CSV)
- **Products**: Variable (from Supabase/CSV)
- **Error Types**: 15 categories
- **Product Categories**: 5 categories
- **Hardware Components**: 48 types

### API
- **Total Endpoints**: 10+
- **Response Time**: <500ms average
- **Concurrent Users**: Supports multiple users

---

## 🔐 Security & Best Practices

- ✅ CORS configured for frontend origins
- ✅ Input validation with Pydantic
- ✅ Error handling and logging
- ✅ Environment variables for sensitive data
- ✅ Optional Supabase integration (falls back to CSV)
- ✅ Model versioning and testing

---

## 📈 Future Enhancements

1. **More Training Data**: Expand datasets for better accuracy
2. **Ensemble Methods**: Combine multiple models for better predictions
3. **User Feedback Loop**: Use feedback to improve models
4. **Real-time Updates**: WebSocket support for live recommendations
5. **Multi-language Support**: Support for multiple languages
6. **Mobile App**: Native mobile application
7. **Analytics Dashboard**: Track recommendation performance
8. **A/B Testing**: Test different recommendation strategies

---

## 📝 Notes

- Models are trained offline and loaded at startup
- Supabase is optional - system works with CSV files
- All models support confidence scores
- Alternative recommendations always provided
- System is designed to be explainable and transparent

---

**Version**: 2.0.0  
**Last Updated**: 2025  
**Status**: Production Ready ✅

