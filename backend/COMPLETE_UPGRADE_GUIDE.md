# Complete Product Need Model Upgrade Guide

## 🎯 Overview

The Product Need Model has been upgraded to handle **real-world user input** including:
- Broken English ("my ps not start", "pc vey slow")
- Very short phrases ("pc slow", "no internet")
- Long natural descriptions
- Typos and informal language
- Multi-component recommendations

## 📋 Implementation Checklist

### ✅ Phase 1: Hierarchical Classification
- [x] Component-to-category mapping (48 components → 6 categories)
- [x] Category model training (5-6 classes)
- [x] Component model training (48 classes, filtered by category)
- [x] Two-stage inference pipeline
- [x] Probability normalization after category filtering

### ✅ Phase 2: Active Learning Loop
- [x] Feedback storage system
- [x] Low confidence threshold (0.5)
- [x] Feedback API endpoint
- [x] Retraining pipeline with feedback
- [x] Model versioning and backup

### ✅ Phase 3: Rule + ML Hybrid
- [x] Rule-based patterns for short inputs
- [x] Broken English handling in rules
- [x] Multi-component rule suggestions
- [x] Rule priority over ML
- [x] Source tracking ("rule", "hierarchical_ml", "ml")

### ✅ Phase 4: Advanced Evaluation
- [x] Top-1 and Top-3 accuracy
- [x] Precision, Recall, F1-score
- [x] Confusion matrix
- [x] Confidence vs Coverage analysis
- [x] Broken English test cases

### ✅ Phase 5: Robust Input Handling
- [x] Data augmentation for broken English
- [x] Character n-grams (3-5) for typos
- [x] Word n-grams (1-2) for context
- [x] Multi-component recommendations
- [x] Grouped by category responses

## 🚀 Quick Start

### Step 1: Augment Training Data (Optional)
```bash
cd backend
.\venv\Scripts\activate
python data_augmentation.py
```

### Step 2: Train Models
```bash
# Train hierarchical models
python train_hierarchical_models.py

# OR train robust models (with broken English handling)
python train_robust_product_need.py
```

### Step 3: Evaluate
```bash
# Evaluate on broken English
python evaluate_broken_english.py

# Evaluate hierarchical vs flat
python evaluate_hierarchical_models.py
```

### Step 4: Start Server
```bash
uvicorn app:app --reload
```

## 📊 Model Architecture

```
User Input (broken English, typos, short phrases)
    ↓
[Rule Matching] → Match? → Return (source: "rule", related components)
    ↓ No match
[Hierarchical ML]
    ├─ Category Model → Predict category (Performance/Power/Network/etc.)
    └─ Component Model → Predict component (filtered by category)
    ↓
[Multi-Component Mapping] → Add related components
    ↓
[Group by Category] → Organize recommendations
    ↓
[Response]
    ├─ Primary recommendation
    ├─ Top 5 alternatives
    ├─ Grouped by category
    └─ ask_feedback: true if confidence < 0.5
```

## 🔧 Feature Engineering

### TF-IDF Configuration
- **Word N-grams**: (1, 2) - Captures context
- **Character N-grams**: (3, 5) - Handles typos
- **min_df**: 1 - Allows rare typos
- **max_df**: 0.95 - Filters common words
- **sublinear_tf**: True - Better scaling
- **stop_words**: 'english' - Removes common words

### Why This Works
- Character n-grams catch "vey" → "very", "slw" → "slow"
- Word n-grams understand "pc slow" → performance issue
- Combined features provide robust understanding

## 📝 API Usage Examples

### Example 1: Broken English
```bash
POST /product_need_recommend
{
  "text": "my ps not start"
}
```

**Response:**
```json
{
  "component": "PSU Upgrade",
  "confidence": 0.95,
  "source": "rule",
  "alternatives": [
    {"label": "PSU Upgrade", "confidence": 0.95},
    {"label": "Power Cable Replacement", "confidence": 0.76}
  ],
  "grouped_by_category": [
    {
      "category": "Power",
      "components": [
        {"label": "PSU Upgrade", "confidence": 0.95},
        {"label": "Power Cable Replacement", "confidence": 0.76}
      ]
    }
  ]
}
```

### Example 2: Short Phrase
```bash
POST /product_need_recommend
{
  "text": "pc slow"
}
```

**Response:**
```json
{
  "component": "RAM Upgrade",
  "confidence": 0.90,
  "source": "rule",
  "alternatives": [
    {"label": "RAM Upgrade", "confidence": 0.90},
    {"label": "SSD Upgrade", "confidence": 0.72},
    {"label": "CPU Upgrade", "confidence": 0.65}
  ],
  "grouped_by_category": [
    {
      "category": "Performance",
      "components": [
        {"label": "RAM Upgrade", "confidence": 0.90},
        {"label": "SSD Upgrade", "confidence": 0.72},
        {"label": "CPU Upgrade", "confidence": 0.65}
      ]
    }
  ]
}
```

### Example 3: Long Description
```bash
POST /product_need_recommend
{
  "text": "my computer takes long time to boot and freezes when I open multiple programs"
}
```

**Response:**
```json
{
  "component": "SSD Upgrade",
  "confidence": 0.85,
  "source": "hierarchical_ml",
  "alternatives": [
    {"label": "SSD Upgrade", "confidence": 0.85},
    {"label": "RAM Upgrade", "confidence": 0.78},
    {"label": "CPU Upgrade", "confidence": 0.45}
  ],
  "grouped_by_category": [
    {
      "category": "Performance",
      "components": [
        {"label": "SSD Upgrade", "confidence": 0.85},
        {"label": "RAM Upgrade", "confidence": 0.78}
      ]
    }
  ]
}
```

## 🔄 Active Learning Workflow

1. **User submits query** → System predicts with confidence
2. **If confidence < 0.5** → `ask_feedback: true` in response
3. **User provides feedback** → Submit via `/product_need_feedback`
4. **Feedback stored** → Saved to `data/product_need_feedback.csv`
5. **Periodic retraining** → Run `retrain_with_feedback.py`
6. **Models improved** → Better accuracy over time

## 📈 Expected Performance

### Rule-Based
- **Accuracy**: ~95% for short, clear inputs
- **Speed**: Instant (no ML inference)
- **Coverage**: ~30-40% of queries

### Hierarchical ML
- **Top-1 Accuracy**: ~85-90%
- **Top-3 Accuracy**: ~95-98%
- **Confidence**: Higher for longer, clearer inputs

### Combined System
- **Overall Accuracy**: ~90%+
- **Robustness**: Handles broken English, typos, short phrases
- **Explainability**: Clear source and grouped recommendations

## 🛠️ Maintenance

### Retrain with Feedback
```bash
python retrain_with_feedback.py
```

### Evaluate Performance
```bash
python evaluate_broken_english.py
python evaluate_hierarchical_models.py
```

### Add New Rules
Edit `backend/rules.py` and add new patterns:
```python
{
    "keywords": "your pattern here",
    "component": "Component Name",
    "confidence": 0.95,
    "explanation": "Why this component",
    "related_components": ["Related Component 1", "Related Component 2"]
}
```

## ✅ Production Readiness

- ✅ Handles real-world input (broken English, typos)
- ✅ Returns multiple recommendations
- ✅ Grouped by category for better UX
- ✅ Active learning for continuous improvement
- ✅ Comprehensive evaluation metrics
- ✅ Lightweight and fast
- ✅ Well-documented and maintainable

---

**Status**: ✅ Production Ready

All requirements implemented and tested. System handles real-world user input robustly!


