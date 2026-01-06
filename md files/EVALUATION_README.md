# Model Evaluation Script

## Overview
This script evaluates the machine learning model performance and generates comprehensive charts showing:
- Accuracy, Precision, Recall, and F1-Score metrics
- Confusion Matrix (both normalized and absolute counts)
- Per-category performance breakdown

## Usage

### Run Evaluation
```bash
cd ml_backend
python evaluate_model.py
```

Or use the batch file:
```bash
evaluate_model.bat
```

## Generated Charts

The script generates the following charts in the `ml_backend/charts/` directory:

1. **metrics_by_category.png** - Bar chart showing Precision, Recall, F1-Score, and Accuracy for each category
2. **overall_metrics.png** - Overall model performance metrics (Accuracy, Precision, Recall, F1-Score)
3. **confusion_matrix_normalized.png** - Normalized confusion matrix showing prediction accuracy
4. **confusion_matrix_absolute.png** - Confusion matrix with absolute counts
5. **f1_score_by_category.png** - Horizontal bar chart of F1-Score by category
6. **precision_recall_f1_comparison.png** - Side-by-side comparison of Precision, Recall, and F1-Score

## Generated Files

- **evaluation_metrics.csv** - Detailed metrics in CSV format for further analysis

## Metrics Explained

- **Accuracy**: Overall percentage of correct predictions
- **Precision**: Percentage of positive predictions that are correct
- **Recall**: Percentage of actual positives that were correctly identified
- **F1-Score**: Harmonic mean of Precision and Recall (balanced metric)

## Model Performance

The evaluation uses a 80/20 train-test split to evaluate the model's ability to:
1. Match user error descriptions to the correct error category
2. Find the most similar error in the database using semantic similarity

## Requirements

- scikit-learn
- matplotlib
- seaborn
- sentence-transformers (already installed)
- numpy
- pandas

Install missing dependencies:
```bash
pip install scikit-learn matplotlib seaborn
```

