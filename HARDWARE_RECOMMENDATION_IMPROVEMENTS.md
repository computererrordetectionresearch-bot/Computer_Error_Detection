# Hardware Recommendation System - Improvements

## Overview
The hardware recommendation system now uses ML models with confidence thresholds and always provides alternative recommendations.

## Key Features

### 1. **Confidence-Based Recommendations**
- **High Confidence (≥0.7)**: Primary recommendation is highly reliable
- **Medium Confidence (0.4-0.7)**: Primary recommendation + alternatives shown
- **Low Confidence (<0.4)**: Multiple alternatives emphasized

### 2. **Always Shows Alternatives**
- Returns top 5 alternative recommendations
- Excludes duplicates
- Shows confidence scores for each alternative
- Helps users make informed decisions

### 3. **Improved ML Model**
- Trained with improved algorithms (SGDClassifier with log_loss)
- 99.6% test accuracy
- Supports probability estimates for confidence scores
- Uses 9,722 training samples across 48 component types

## API Endpoint

### `/product_need_recommend`

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
  "definition": "RAM (Random Access Memory) is...",
  "why_useful": "More RAM helps...",
  "extra_explanation": "Based on your description, RAM Upgrade is highly recommended...",
  "alternatives": [
    {"label": "RAM Upgrade", "confidence": 0.865},
    {"label": "SSD Upgrade", "confidence": 0.082},
    {"label": "CPU Upgrade", "confidence": 0.015}
  ],
  "is_low_confidence": false
}
```

## Confidence Thresholds

| Confidence Level | Behavior |
|-----------------|----------|
| **≥ 0.7 (High)** | Primary recommendation is shown with high confidence message |
| **0.4 - 0.7 (Medium)** | Primary recommendation shown with "likely" message, alternatives emphasized |
| **< 0.4 (Low)** | Primary shown but marked as low confidence, alternatives strongly emphasized |

## Training the Model

To retrain the improved model:

```bash
cd backend
.\venv\Scripts\activate
python train_improved_models.py
```

This will:
- Test multiple algorithms (LogisticRegression, SGDClassifier, MultinomialNB)
- Use cross-validation to select the best
- Train on the full dataset
- Save the best model to `product_need_model.pkl`

## Model Performance

- **Test Accuracy**: 99.6%
- **Training Samples**: 9,722
- **Component Types**: 48
- **Algorithm**: SGDClassifier with log_loss
- **Vectorization**: TF-IDF with n-grams (1,2)

## Usage Examples

### High Confidence Example
```
Input: "I need more RAM for multitasking"
Output: 
  - Primary: RAM Upgrade (confidence: 0.96)
  - Alternatives: Laptop RAM Upgrade, RAM Slot Cleaning
```

### Medium Confidence Example
```
Input: "Computer is slow"
Output:
  - Primary: RAM Upgrade (confidence: 0.55)
  - Alternatives: SSD Upgrade, CPU Upgrade, GPU Upgrade
  - Message: "likely what you need, but consider alternatives"
```

### Low Confidence Example
```
Input: "Something is wrong"
Output:
  - Primary: General Repair (confidence: 0.25)
  - Alternatives: Multiple options shown
  - Message: "not very confident, please review alternatives"
```

## Benefits

1. **Better User Experience**: Users always see multiple options
2. **Transparency**: Confidence scores help users understand reliability
3. **Flexibility**: Works well even with ambiguous inputs
4. **Accuracy**: 99.6% accuracy on test set
5. **Robustness**: Handles edge cases gracefully

## Future Improvements

1. Add more training data for rare component types
2. Implement ensemble methods for even better accuracy
3. Add user feedback loop to improve model over time
4. Integrate with product catalog for direct purchase links

