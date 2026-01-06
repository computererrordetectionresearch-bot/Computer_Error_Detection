# Complete Guide to the PC Recommendation Engine

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Core Components](#core-components)
4. [Machine Learning Models](#machine-learning-models)
5. [API Endpoints](#api-endpoints)
6. [Data Flow](#data-flow)
7. [Key Features](#key-features)
8. [Technology Stack](#technology-stack)
9. [How It Works](#how-it-works)
10. [Training & Evaluation](#training--evaluation)
11. [Frontend Integration](#frontend-integration)
12. [Usage Examples](#usage-examples)

---

## Overview

The **PC Recommendation Engine** is an intelligent, full-stack system that helps users find:
- **Repair Shops** - Based on error type, location, budget, and urgency
- **Hardware Products** - Based on symptoms and component needs
- **Tools & Software** - For DIY repairs and diagnostics

### What Makes It Intelligent?

1. **ML-Powered Classification**: Uses NLP models to understand user queries
2. **Hierarchical Inference**: Two-stage prediction (Category → Component) for better accuracy
3. **Rule-Based Safety Layer**: High-confidence pattern matching before ML inference
4. **Explainable Recommendations**: Provides reasons for each recommendation
5. **Active Learning**: Collects feedback on low-confidence predictions
6. **Spell Checking**: Automatically corrects typos in user input

---

## System Architecture

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
│  │    ML Models Layer                                   │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐              │  │
│  │  │  Shop    │ │  Error   │ │ Product  │              │  │
│  │  │ Ranking  │ │  Type    │ │  Need    │              │  │
│  │  │  Model   │ │   NLP    │ │   NLP    │              │  │
│  │  └──────────┘ └──────────┘ └──────────┘              │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                               │
│  ┌─────────────────────────┼────────────────────────────┐  │
│  │      Data Layer                                      │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐              │  │
│  │  │ Supabase │ │   CSV    │ │  Models  │              │  │
│  │  │  (DB)    │ │  Files   │ │   (.pkl) │              │  │
│  │  └──────────┘ └──────────┘ └──────────┘              │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. **Backend (`backend/app.py`)**
The main FastAPI application that handles all API requests and orchestrates ML inference.

**Key Responsibilities:**
- API endpoint management
- Request validation
- ML model orchestration
- Business logic (feature engineering, ranking)
- Data access (Supabase or CSV fallback)

### 2. **Hierarchical Inference System (`backend/hierarchical_inference.py`)**
Two-stage prediction system for hardware component recommendations:
- **Stage 1**: Predict product category (e.g., "Storage", "Memory", "Graphics")
- **Stage 2**: Predict specific component within that category (e.g., "SSD Upgrade")

**Benefits:**
- Better accuracy by filtering components by category
- More explainable predictions
- Handles 53 component types across multiple categories

### 3. **Rule-Based Matching (`backend/rules.py`)**
High-confidence pattern matching system that matches user queries to hardware components before ML inference.

**Features:**
- 100+ predefined rules for common issues
- Returns high confidence (0.88-0.95) for matched patterns
- Provides explanations and related components
- Faster than ML inference for common queries

**Example Rules:**
- "pc slow" → RAM Upgrade (90% confidence)
- "no power" → PSU Upgrade (95% confidence)
- "camera not working" → Webcam Upgrade (95% confidence)

### 4. **Spell Checker (`backend/spell_checker.py`)**
Automatically detects and corrects typos in user input to improve ML accuracy.

### 5. **Feedback Storage (`backend/feedback_storage.py`)**
Collects user feedback on low-confidence predictions for active learning and model improvement.

### 6. **Frontend (`frontend/`)**
Next.js 15 application with three main tabs:
- **Repairs Tab**: Find repair shops
- **Products Tab**: Find hardware products
- **Tools Tab**: Find diagnostic tools

---

## Machine Learning Models

The system uses **4 trained ML models**:

### 1. **Shop Ranking Model** (`reco_model.pkl`)
- **Type**: Gradient Boosting Classifier
- **Purpose**: Ranks repair shops based on multiple features
- **Features Used**:
  - Quality metrics (rating, reviews, verified status)
  - Match indicators (district, shop type, budget fit)
  - Urgency penalty
- **Output**: Shop ranking scores (0-100%)

### 2. **Error Type NLP Model** (`nlp_error_model_error_type.pkl`)
- **Type**: SGDClassifier with log_loss
- **Purpose**: Classifies error type from free-text descriptions
- **Classes**: 21 error types (e.g., "GPU Overheat", "Blue Screen", "Boot Device Error")
- **Performance**:
  - Accuracy: **83.70%**
  - Precision: **83.75%**
  - Recall: **83.70%**
  - F1-Score: **83.44%**
  - MAP: **86.00%**
- **Training Data**: 3,219 samples (2,575 training, 644 test)

### 3. **Product Category NLP Model** (`nlp_error_model_product.pkl`)
- **Type**: SGDClassifier
- **Purpose**: Classifies product category from symptoms
- **Classes**: 3 categories
- **Performance**:
  - Accuracy: **66.67%**
  - MAP: **100.00%**
- **Note**: Limited by small dataset (14 samples)

### 4. **Product Need Model** (`product_need_model.pkl`)
- **Type**: SGDClassifier with log_loss
- **Purpose**: Recommends specific hardware components
- **Classes**: 53 component types (e.g., "RAM Upgrade", "SSD Upgrade", "GPU Upgrade")
- **Performance**:
  - Accuracy: **97.79%** ⭐
  - Precision: **97.43%**
  - Recall: **97.79%**
  - F1-Score: **97.60%**
  - MAP: **71.09%**
- **Training Data**: 22,443 samples (17,954 training, 4,489 test)

### Model Inference Flow

For hardware component recommendations:

```
User Input: "My PC is very slow"
    │
    ├─→ [1] Rule-Based Matching
    │      └─→ Match? → Return (High Confidence)
    │
    ├─→ [2] Hierarchical ML (if no rule match)
    │      ├─→ Stage 1: Predict Category (e.g., "Memory")
    │      └─→ Stage 2: Predict Component in Category (e.g., "RAM Upgrade")
    │
    └─→ [3] Flat ML Model (fallback)
           └─→ Direct component prediction
```

---

## API Endpoints

### **Recommendation Endpoints**

#### `POST /rank_auto`
Automatically finds and ranks repair shops based on error type, budget, urgency, and location.

**Request:**
```json
{
  "error_type": "GPU Overheat",
  "budget": "medium",
  "urgency": "high",
  "user_district": "Colombo"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "shop_id": "1",
      "shop_name": "TechFix Solutions",
      "score": 92.5,
      "district": "Colombo",
      "avg_rating": 4.8,
      "reviews": 150,
      "verified": true,
      "reason": "High-rated shop in your district specializing in GPU repairs",
      "factors": ["District Match", "High Rating", "Specialization"]
    }
  ],
  "summary": "Found 10 shops matching your criteria..."
}
```

#### `POST /product_need_recommend`
Recommends hardware components using hierarchical ML + rule-based system.

**Request:**
```json
{
  "text": "My PC is very slow and takes forever to boot"
}
```

**Response:**
```json
{
  "recommended_component": "SSD Upgrade",
  "confidence": 0.91,
  "source": "hierarchical_ml",
  "explanation": "Slow boot times indicate storage bottleneck. Upgrade to SSD for faster startup.",
  "alternatives": [
    {"label": "SSD Upgrade", "confidence": 0.91},
    {"label": "RAM Upgrade", "confidence": 0.75}
  ],
  "grouped_by_category": {
    "Storage": [{"label": "SSD Upgrade", "confidence": 0.91}],
    "Memory": [{"label": "RAM Upgrade", "confidence": 0.75}]
  },
  "spell_correction": null,
  "needs_feedback": false
}
```

#### `POST /rank_products_auto`
Finds and ranks hardware products based on product type, budget, and location.

#### `GET /tools_recommend`
Recommends diagnostic tools and software based on error type.

### **NLP Endpoints**

#### `POST /nlp/detect_error_type`
Detects error type from free-text description using hybrid system (rules + ML).

**Request:**
```json
{
  "text": "My computer keeps showing a blue screen and restarting"
}
```

**Response:**
```json
{
  "label": "Blue Screen",
  "confidence": 0.89,
  "source": "ml",
  "alternatives": [
    {"label": "Blue Screen", "confidence": 0.89},
    {"label": "OS Reinstall / Corrupted", "confidence": 0.12}
  ],
  "similar_errors": [
    {"label": "Boot Device Error", "confidence": 0.65}
  ],
  "explanation": "Blue screen errors typically indicate hardware or driver issues..."
}
```

#### `POST /nlp/detect_product_category`
Detects product category from symptom description.

### **Details Endpoints**

#### `GET /shop_details?shop_id={id}`
Returns detailed information about a specific shop.

#### `GET /product_details?product_id={id}`
Returns detailed information about a specific product.

#### `GET /tool_details?tool_id={id}`
Returns detailed information about a specific tool.

### **Feedback Endpoints**

#### `POST /feedback`
Submits user feedback on recommendations.

#### `POST /product_need_feedback`
Submits feedback specifically for hardware component recommendations.

### **Utility Endpoints**

#### `GET /`
API information and status.

#### `GET /health/supabase`
Checks Supabase connection status.

#### `POST /full_recommendation`
Returns comprehensive recommendations (shops + products + tools) in one request.

---

## Data Flow

### 1. **User Input Flow**
```
User enters query → Frontend validates → API request → Backend processes
```

### 2. **Shop Recommendation Flow**
```
User Query
    │
    ├─→ Detect Error Type (NLP Model)
    │      └─→ "GPU Overheat"
    │
    ├─→ Fetch Candidate Shops (from DB/CSV)
    │      └─→ Filter by error type, district
    │
    ├─→ Feature Engineering
    │      ├─→ Calculate district_match
    │      ├─→ Calculate type_match
    │      ├─→ Calculate budget_fit
    │      └─→ Apply urgency penalty
    │
    ├─→ ML Ranking (Gradient Boosting)
    │      └─→ Score each shop (0-100)
    │
    ├─→ Generate Explanations
    │      └─→ "High-rated shop in your district..."
    │
    └─→ Return Ranked Recommendations
```

### 3. **Hardware Component Recommendation Flow**
```
User Query: "PC is slow"
    │
    ├─→ [1] Spell Check
    │      └─→ Correct typos if any
    │
    ├─→ [2] Rule-Based Matching
    │      └─→ Match "pc slow" → "RAM Upgrade" (90% confidence)
    │      └─→ Return if matched
    │
    ├─→ [3] Hierarchical ML (if no rule match)
    │      ├─→ Stage 1: Predict Category → "Memory"
    │      └─→ Stage 2: Predict Component → "RAM Upgrade" (filtered by Memory category)
    │
    ├─→ [4] Get Alternatives
    │      └─→ Top 5 components with confidence scores
    │
    ├─→ [5] Group by Category
    │      └─→ Organize alternatives by category
    │
    └─→ [6] Return Recommendation
           ├─→ Primary component
           ├─→ Confidence score
           ├─→ Explanation
           ├─→ Alternatives
           └─→ Grouped by category
```

---

## Key Features

### 1. **Explainable Recommendations**
Every recommendation includes:
- **Reason**: Why this shop/product was recommended
- **Factors**: Key factors that influenced the recommendation
- **Confidence Score**: How confident the system is (0-100%)

### 2. **Multi-Criteria Filtering**
- **Location**: District-based matching
- **Budget**: Low, Medium, High budget filtering
- **Urgency**: Adjusts recommendations based on urgency
- **Verified Shops**: Filter for verified shops only
- **Open Now**: Filter for currently open shops

### 3. **Confidence Thresholds**
- **High Confidence** (≥0.7): Strong recommendation
- **Medium Confidence** (0.4-0.7): Good recommendation with alternatives
- **Low Confidence** (<0.4): Requests user feedback for improvement

### 4. **Active Learning**
- Collects feedback on low-confidence predictions
- Stores feedback for model retraining
- Improves accuracy over time

### 5. **Spell Checking**
- Automatically detects typos
- Suggests corrections
- Uses corrected text for better ML accuracy

### 6. **Alternative Recommendations**
- Always provides top 5 alternatives
- Grouped by category for better organization
- Shows confidence scores for each alternative

### 7. **Hierarchical Inference**
- Two-stage prediction improves accuracy
- Category filtering reduces false positives
- More explainable predictions

### 8. **Rule-Based Safety Layer**
- Fast pattern matching for common queries
- High confidence for matched patterns
- Provides explanations and related components

---

## Technology Stack

### **Backend**
- **Framework**: FastAPI (Python 3.13+)
- **ML Library**: Scikit-learn
- **Vectorization**: TF-IDF
- **Data Processing**: Pandas, NumPy
- **Database**: Supabase (optional, falls back to CSV)
- **Model Serialization**: Joblib

### **Frontend**
- **Framework**: Next.js 15.5.4
- **UI Library**: React 19.1.0
- **Styling**: Tailwind CSS
- **Components**: Radix UI
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Type Safety**: TypeScript

### **ML Models**
- **Shop Ranking**: Gradient Boosting Classifier
- **Error Type**: SGDClassifier with log_loss
- **Product Category**: SGDClassifier
- **Product Need**: SGDClassifier with log_loss

---

## How It Works

### **Step-by-Step: Shop Recommendation**

1. **User Input**: User describes their problem or selects an error type
2. **Error Detection**: System uses NLP to detect error type from text (if needed)
3. **Candidate Fetching**: System fetches shops from database/CSV that match the error type
4. **Feature Engineering**: System calculates features for each shop:
   - District match (1 if same district, 0 otherwise)
   - Type match (1 if shop specializes in error type, 0 otherwise)
   - Budget fit (1 if shop fits budget, 0 otherwise)
   - Quality score (based on rating, reviews, verified status)
   - Urgency penalty (reduces score if turnaround time is too long)
5. **ML Ranking**: Gradient Boosting model scores each shop (0-100)
6. **Explanation Generation**: System generates human-readable explanations
7. **Response**: Returns ranked list with explanations and confidence scores

### **Step-by-Step: Hardware Component Recommendation**

1. **User Input**: User describes their problem (e.g., "PC is slow")
2. **Spell Check**: System corrects any typos
3. **Rule Matching**: System checks if query matches any predefined rules
   - If match found: Return immediately with high confidence
4. **Hierarchical ML** (if no rule match):
   - Stage 1: Predict product category (e.g., "Memory")
   - Stage 2: Predict component within category (e.g., "RAM Upgrade")
5. **Get Alternatives**: System finds top 5 alternative components
6. **Group by Category**: Organizes alternatives by category
7. **Response**: Returns recommendation with confidence, explanation, and alternatives

---

## Training & Evaluation

### **Training Scripts**

1. **`train_improved_nlp_models.py`**: Enhanced NLP models with better preprocessing
2. **`train_product_need_improved.py`**: Improved product need model training

### **Training Data**

- **Error Type Model**: `error_training_data_combined.csv` (3,219 samples, 21 error types)
- **Product Need Model**: `hardware_component_dataset_combined.csv` (22,443 samples, 53 components)
- **Product Category Model**: `product_texts.csv` (14 samples, 5 categories)

### **Evaluation**

Run comprehensive model evaluation:
```bash
cd backend
python evaluate_models_with_visualization.py
```

**Generated Visualizations:**
- Performance metrics comparison
- Individual metric comparisons
- Radar charts
- Metrics heatmap
- Confusion matrices (raw and normalized)
- Summary tables

**Evaluation Results Location**: `backend/model_evaluations/`

### **Model Performance Summary**

| Model | Accuracy | Precision | Recall | F1-Score | MAP |
|-------|----------|-----------|--------|----------|-----|
| **Error Type** | 83.70% | 83.75% | 83.70% | 83.44% | 86.00% |
| **Product Category** | 66.67% | 66.67% | 66.67% | 66.67% | 100.00% |
| **Product Need** | **97.79%** ⭐ | **97.43%** ⭐ | **97.79%** ⭐ | **97.60%** ⭐ | 71.09% |

---

## Frontend Integration

### **Main Components**

1. **`QueryBar`**: Input field for user queries with speech-to-text support
2. **`RecommendationCard`**: Displays shop/product recommendations
3. **`ErrorSuggestions`**: Shows error type suggestions
4. **`ProductCard`**: Displays product recommendations
5. **`ToolCard`**: Displays tool recommendations
6. **`FeedbackModal`**: Collects user feedback
7. **`SmartFixPlan`**: Shows step-by-step fix plans

### **API Integration**

Frontend uses `src/lib/api.ts` for all API calls:
- `searchRepairs()`: Search for repair shops
- `searchProductsAuto()`: Search for products
- `getToolsRecommendation()`: Get tool recommendations
- `submitFeedback()`: Submit user feedback

### **State Management**

- React hooks for state management
- Local state for form data
- API state for loading/error handling

---

## Usage Examples

### **Example 1: Finding a Repair Shop**

**Frontend Request:**
```typescript
const response = await searchRepairs({
  error_type: "GPU Overheat",
  budget: "medium",
  urgency: "high",
  user_district: "Colombo"
});
```

**Backend Processing:**
1. Detects error type: "GPU Overheat"
2. Fetches shops that handle GPU issues
3. Filters by district: "Colombo"
4. Calculates features (district match, budget fit, etc.)
5. Ranks using ML model
6. Returns top 10 shops with explanations

### **Example 2: Hardware Component Recommendation**

**Frontend Request:**
```typescript
const response = await fetch('http://localhost:8000/product_need_recommend', {
  method: 'POST',
  body: JSON.stringify({ text: "My PC is very slow" })
});
```

**Backend Processing:**
1. Spell checks: "My PC is very slow" (no corrections needed)
2. Rule matching: Matches "pc slow" → "RAM Upgrade" (90% confidence)
3. Returns immediately with:
   - Component: "RAM Upgrade"
   - Confidence: 0.90
   - Explanation: "Slow PC often needs RAM or SSD upgrade."
   - Alternatives: ["SSD Upgrade", "CPU Upgrade"]

### **Example 3: Error Type Detection**

**Frontend Request:**
```typescript
const response = await fetch('http://localhost:8000/nlp/detect_error_type', {
  method: 'POST',
  body: JSON.stringify({ text: "My computer keeps restarting with a blue screen" })
});
```

**Backend Processing:**
1. Preprocesses text
2. Runs NLP model
3. Returns:
   - Label: "Blue Screen"
   - Confidence: 0.89
   - Source: "ml"
   - Alternatives: Top 3 predictions
   - Similar errors: Related error types

---

## Configuration

### **Environment Variables**

Create `.env` file in `backend/`:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### **Model Files**

Ensure these model files exist in `backend/`:
- `reco_model.pkl` - Shop ranking model
- `nlp_error_model_error_type.pkl` - Error type classification
- `nlp_error_model_product.pkl` - Product category classification
- `product_need_model.pkl` - Product need classification
- `product_need_category_model.pkl` - Category prediction (for hierarchical)
- `product_need_component_model.pkl` - Component prediction (for hierarchical)

### **Data Files**

Ensure these CSV files exist in `data/`:
- `shops.csv` - Shop data
- `products.csv` - Product data
- `error_training_data_combined.csv` - Error training data
- `hardware_component_dataset_combined.csv` - Component training data

---

## Best Practices

### **For Developers**

1. **Always check confidence scores** before displaying recommendations
2. **Request feedback** for low-confidence predictions (<0.5)
3. **Use spell checking** before ML inference
4. **Cache model predictions** for common queries
5. **Monitor model performance** in production

### **For Users**

1. **Be specific** in problem descriptions for better accuracy
2. **Provide feedback** to improve the system
3. **Check alternatives** if primary recommendation doesn't fit
4. **Review explanations** to understand recommendations

---

## Troubleshooting

### **Common Issues**

1. **Low Confidence Predictions**
   - Solution: Collect more training data for rare cases
   - Use rule-based patterns for common issues

2. **Model Not Loading**
   - Check if `.pkl` files exist in `backend/`
   - Verify file permissions

3. **Supabase Connection Failed**
   - System automatically falls back to CSV files
   - Check `.env` file for correct credentials

4. **Frontend Not Connecting**
   - Verify backend is running on port 8000
   - Check CORS configuration in `app.py`

---

## Future Improvements

1. **More Training Data**: Collect more samples for Product Category model
2. **Real-time Learning**: Implement online learning for continuous improvement
3. **Multi-language Support**: Add support for multiple languages
4. **Advanced Features**: Add price prediction, availability checking
5. **Mobile App**: Develop mobile application
6. **Recommendation History**: Track user history for personalized recommendations

---

## Conclusion

The PC Recommendation Engine is a comprehensive, intelligent system that combines:
- **Machine Learning** for accurate predictions
- **Rule-Based Systems** for fast, high-confidence matches
- **Hierarchical Inference** for better accuracy
- **Explainable AI** for user trust
- **Active Learning** for continuous improvement

The system is production-ready and can handle real-world queries with high accuracy, especially for hardware component recommendations (97.79% accuracy).

---

**Last Updated**: 2026-01-02  
**Version**: 2.0.0  
**Status**: Production Ready



