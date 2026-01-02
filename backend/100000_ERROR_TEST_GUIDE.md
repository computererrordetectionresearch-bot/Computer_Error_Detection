# 100,000 Error Test and Model Retraining Guide

## Overview

This system has been enhanced to:
1. Test with 100,000 different PC error scenarios
2. Evaluate both error classification and hardware recommendation accuracy
3. Automatically identify incorrect predictions
4. Retrain models with corrections
5. Support multiple error types per error (show all applicable types to users)

## Features

### 1. Multiple Error Type Detection
- The system now detects when an error description contains multiple error types
- Multiple primary error types are shown to users (not just alternatives)
- Example: "PC slow CPU hot and need more RAM" → detects both "CPU Overheat" and "RAM Upgrade"

### 2. Comprehensive Testing
- Tests 100,000 different error scenarios
- Includes both single and multi-error type cases
- Evaluates both error classification and hardware recommendation
- Generates detailed accuracy reports

### 3. Automatic Model Retraining
- Identifies incorrect predictions
- Creates corrected training datasets
- Retrains both error classification and hardware recommendation models
- Backs up old models before retraining

## Files Created

### Test Generation
- `create_100000_test_errors.py` - Generates 100,000 test error scenarios
- `test_100000_errors_comprehensive.py` - Tests both error classification and hardware recommendation

### Model Retraining
- `retrain_from_100000_test.py` - Retrains models with corrections

### Master Script
- `run_100000_test_and_retrain.py` - Runs the complete workflow

## Usage

### Quick Start - Automated (Recommended)

**Automatically test and retrain if wrong predictions found:**

```bash
cd backend
python auto_test_and_retrain.py
```

Or on Windows:
```bash
cd backend
auto_test_and_retrain.bat
```

This will:
1. Create 100,000 test errors (if not exists)
2. Test error classification and hardware recommendation
3. **Automatically check for incorrect predictions**
4. **Automatically retrain models if corrections are found**
5. Skip retraining if all predictions are correct

### Manual Workflow

Run the master script to execute the complete workflow manually:

```bash
cd backend
python run_100000_test_and_retrain.py
```

This will:
1. Create 100,000 test errors (if not exists)
2. Test error classification and hardware recommendation
3. Retrain models with corrections

### Step-by-Step

#### Step 1: Create Test Dataset

```bash
cd backend
python create_100000_test_errors.py
```

This creates `data/test_100000_errors.csv` with:
- ~80,000 single error type samples
- ~20,000 multi-error type samples
- Total: 100,000 test scenarios

#### Step 2: Run Tests

```bash
cd backend
python test_100000_errors_comprehensive.py
```

This will:
- Test error classification on all 100,000 samples
- Test hardware recommendation on 10,000 samples (for speed)
- Generate accuracy reports
- Save incorrect predictions to:
  - `data/incorrect_error_predictions_100000.csv`
  - `data/incorrect_hardware_predictions_100000.csv`

#### Step 3: Retrain Models

```bash
cd backend
python retrain_from_100000_test.py
```

This will:
- Load all existing training data
- Add corrected predictions from test results
- Retrain error classification model
- Retrain hardware recommendation model
- Backup old models before saving new ones

## Output Files

### Test Results
- `data/test_100000_errors.csv` - Test dataset
- `data/incorrect_error_predictions_100000.csv` - Incorrect error classifications (for retraining)
- `data/incorrect_hardware_predictions_100000.csv` - Incorrect hardware recommendations (for retraining)
- `backend/test_100000_results_summary.json` - Test summary with accuracy metrics

### Model Backups
- `backend/nlp_error_model_error_type_backup_YYYYMMDD_HHMMSS.pkl` - Backup of error model
- `backend/product_need_model_backup_YYYYMMDD_HHMMSS.pkl` - Backup of hardware model

## API Changes

### Error Detection Endpoint

The `/nlp/detect_error_type` endpoint now returns:

```json
{
  "label": "CPU Overheat",
  "confidence": 0.85,
  "source": "ml",
  "alternatives": [...],
  "similar_errors": [...],
  "explanation": "...",
  "multiple_types": [
    {
      "label": "CPU Overheat",
      "confidence": 0.85
    },
    {
      "label": "Slow Performance",
      "confidence": 0.72
    }
  ]
}
```

### Frontend Display

The frontend now displays multiple error types when detected:
- Shows an orange warning box with all detected error types
- Each type shows its confidence score
- Users can see all applicable issues at once

## Model Accuracy

After retraining, you should see improved accuracy:
- Error Classification: Target >90% accuracy
- Hardware Recommendation: Target >95% accuracy
- Multi-Error Detection: Improved coverage of complex scenarios

## Troubleshooting

### Test Dataset Already Exists
If `data/test_100000_errors.csv` exists, the script will skip generation.
Delete the file to regenerate.

### Out of Memory
If you encounter memory issues:
- Reduce test size in `test_100000_errors_comprehensive.py`
- Test in batches
- Use a machine with more RAM

### Model Loading Issues
After retraining:
1. **Restart the backend server** to load new models
2. Check that model files exist in `backend/` directory
3. Verify model file sizes are reasonable (>1MB)

## Best Practices

1. **Run tests regularly** to catch model degradation
2. **Review incorrect predictions** before retraining
3. **Backup models** before retraining (automatic)
4. **Monitor accuracy** trends over time
5. **Update test dataset** with new error patterns

## Next Steps

1. Run the complete workflow: `python run_100000_test_and_retrain.py`
2. Review test results in `test_100000_results_summary.json`
3. Check incorrect predictions files
4. Restart backend server after retraining
5. Test the system with real user queries

## Notes

- The test may take 30-60 minutes depending on your system
- Retraining may take 10-20 minutes
- Models are automatically backed up before retraining
- Frontend automatically displays multiple error types when detected

