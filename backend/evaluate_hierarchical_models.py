"""
Advanced evaluation metrics for hierarchical Product Need Models.
Compares flat vs hierarchical approach with comprehensive metrics.
"""

from pathlib import Path
import pandas as pd
import joblib
import json
import sys
import io
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

# Model paths
FLAT_MODEL_PATH = HERE / "product_need_model.pkl"  # Old flat model
CATEGORY_MODEL_PATH = HERE / "product_need_category_model.pkl"
COMPONENT_MODEL_PATH = HERE / "product_need_component_model.pkl"
MAPPING_PATH = HERE / "component_category_mapping.json"

# Import hierarchical inference
from hierarchical_inference import predict_hierarchical, _load_models


def load_test_data():
    """Load test data from hardware dataset."""
    HARDWARE_CSV = DATA_DIR / "hardware_component_dataset_merged.csv"
    df = pd.read_csv(HARDWARE_CSV)
    df = df.dropna(subset=['user_text', 'component_label'])
    df['text'] = df['user_text'].astype(str).str.lower().str.strip()
    df = df[df['text'].str.len() > 0]
    
    # Split into train/test (use same split as training)
    from sklearn.model_selection import train_test_split
    _, df_test = train_test_split(df, test_size=0.2, random_state=42)
    
    return df_test


def evaluate_flat_model(df_test: pd.DataFrame) -> Dict:
    """Evaluate the old flat model."""
    if not FLAT_MODEL_PATH.exists():
        return {"error": "Flat model not found"}
    
    model = joblib.load(FLAT_MODEL_PATH)
    
    y_true = df_test['component_label'].values
    y_pred = []
    y_proba_top3 = []
    
    for text in df_test['text'].values:
        try:
            pred = model.predict([text])[0]
            proba = model.predict_proba([text])[0]
            classes = model.classes_
            
            # Get top 3
            top3_idx = np.argsort(proba)[::-1][:3]
            top3 = [(classes[i], proba[i]) for i in top3_idx]
            
            y_pred.append(pred)
            y_proba_top3.append(top3)
        except:
            y_pred.append(None)
            y_proba_top3.append([])
    
    # Filter out None predictions
    valid_mask = [p is not None for p in y_pred]
    y_true_valid = [y_true[i] for i in range(len(y_true)) if valid_mask[i]]
    y_pred_valid = [y_pred[i] for i in range(len(y_pred)) if valid_mask[i]]
    
    if not y_pred_valid:
        return {"error": "No valid predictions"}
    
    accuracy = accuracy_score(y_true_valid, y_pred_valid)
    
    # Top-3 accuracy
    top3_correct = 0
    for i, (true_label, top3) in enumerate(zip(y_true_valid, [y_proba_top3[j] for j in range(len(y_proba_top3)) if valid_mask[j]])):
        if any(label == true_label for label, _ in top3[:3]):
            top3_correct += 1
    top3_accuracy = top3_correct / len(y_true_valid) if y_true_valid else 0
    
    # Per-class metrics
    unique_labels = sorted(set(y_true_valid + y_pred_valid))
    precision = precision_score(y_true_valid, y_pred_valid, labels=unique_labels, average='weighted', zero_division=0)
    recall = recall_score(y_true_valid, y_pred_valid, labels=unique_labels, average='weighted', zero_division=0)
    f1 = f1_score(y_true_valid, y_pred_valid, labels=unique_labels, average='weighted', zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(y_true_valid, y_pred_valid, labels=unique_labels)
    
    return {
        "accuracy": accuracy,
        "top3_accuracy": top3_accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": cm,
        "labels": unique_labels,
        "n_samples": len(y_true_valid)
    }


def evaluate_hierarchical_model(df_test: pd.DataFrame) -> Dict:
    """Evaluate the new hierarchical model."""
    if not CATEGORY_MODEL_PATH.exists() or not COMPONENT_MODEL_PATH.exists():
        return {"error": "Hierarchical models not found"}
    
    y_true = df_test['component_label'].values
    y_pred = []
    y_proba_top3 = []
    y_category_pred = []
    
    for text in df_test['text'].values:
        try:
            comp, conf, source, top5 = predict_hierarchical(text)
            y_pred.append(comp)
            
            # Get top 3 from alternatives
            top3 = top5[:3] if len(top5) >= 3 else top5
            y_proba_top3.append(top3)
            
            # Get category prediction
            category_model, _, _, _ = _load_models()
            if category_model:
                cat_pred = category_model.predict([text])[0]
                y_category_pred.append(cat_pred)
            else:
                y_category_pred.append(None)
        except Exception as e:
            y_pred.append(None)
            y_proba_top3.append([])
            y_category_pred.append(None)
    
    # Filter out None predictions
    valid_mask = [p is not None for p in y_pred]
    y_true_valid = [y_true[i] for i in range(len(y_true)) if valid_mask[i]]
    y_pred_valid = [y_pred[i] for i in range(len(y_pred)) if valid_mask[i]]
    
    if not y_pred_valid:
        return {"error": "No valid predictions"}
    
    accuracy = accuracy_score(y_true_valid, y_pred_valid)
    
    # Top-3 accuracy
    top3_correct = 0
    for i, (true_label, top3) in enumerate(zip(y_true_valid, [y_proba_top3[j] for j in range(len(y_proba_top3)) if valid_mask[j]])):
        if any(label == true_label for label, _ in top3[:3]):
            top3_correct += 1
    top3_accuracy = top3_correct / len(y_true_valid) if y_true_valid else 0
    
    # Per-class metrics
    unique_labels = sorted(set(y_true_valid + y_pred_valid))
    precision = precision_score(y_true_valid, y_pred_valid, labels=unique_labels, average='weighted', zero_division=0)
    recall = recall_score(y_true_valid, y_pred_valid, labels=unique_labels, average='weighted', zero_division=0)
    f1 = f1_score(y_true_valid, y_pred_valid, labels=unique_labels, average='weighted', zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(y_true_valid, y_pred_valid, labels=unique_labels)
    
    return {
        "accuracy": accuracy,
        "top3_accuracy": top3_accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": cm,
        "labels": unique_labels,
        "n_samples": len(y_true_valid),
        "category_predictions": y_category_pred
    }


def confidence_vs_coverage(y_true: List, y_pred: List, y_proba_top3: List, thresholds: List[float] = [0.3, 0.5, 0.7, 0.9]) -> pd.DataFrame:
    """Calculate coverage and accuracy at different confidence thresholds."""
    results = []
    
    for threshold in thresholds:
        covered = 0
        correct = 0
        
        for i, (true_label, top3) in enumerate(zip(y_true, y_proba_top3)):
            if top3 and top3[0][1] >= threshold:  # Top prediction confidence
                covered += 1
                if top3[0][0] == true_label:
                    correct += 1
        
        coverage = covered / len(y_true) if y_true else 0
        accuracy_at_threshold = correct / covered if covered > 0 else 0
        
        results.append({
            "confidence_threshold": threshold,
            "coverage": coverage,
            "accuracy": accuracy_at_threshold,
            "n_covered": covered
        })
    
    return pd.DataFrame(results)


def print_comparison(flat_results: Dict, hierarchical_results: Dict):
    """Print comparison table."""
    print("\n" + "=" * 80)
    print("MODEL COMPARISON: FLAT vs HIERARCHICAL")
    print("=" * 80)
    
    if "error" in flat_results or "error" in hierarchical_results:
        if "error" in flat_results:
            print(f"❌ Flat model: {flat_results['error']}")
        if "error" in hierarchical_results:
            print(f"❌ Hierarchical model: {hierarchical_results['error']}")
        return
    
    print(f"\n{'Metric':<25} {'Flat Model':<20} {'Hierarchical Model':<20} {'Improvement':<15}")
    print("-" * 80)
    
    metrics = [
        ("Accuracy", "accuracy", "{:.4f}"),
        ("Top-3 Accuracy", "top3_accuracy", "{:.4f}"),
        ("Precision", "precision", "{:.4f}"),
        ("Recall", "recall", "{:.4f}"),
        ("F1-Score", "f1", "{:.4f}"),
    ]
    
    for metric_name, key, fmt in metrics:
        flat_val = flat_results.get(key, 0)
        hier_val = hierarchical_results.get(key, 0)
        improvement = hier_val - flat_val
        improvement_str = f"+{improvement:.4f}" if improvement >= 0 else f"{improvement:.4f}"
        
        print(f"{metric_name:<25} {fmt.format(flat_val):<20} {fmt.format(hier_val):<20} {improvement_str:<15}")
    
    print(f"\n{'Samples':<25} {flat_results.get('n_samples', 0):<20} {hierarchical_results.get('n_samples', 0):<20}")


def save_metrics_to_csv(flat_results: Dict, hierarchical_results: Dict, output_path: Path):
    """Save metrics to CSV."""
    rows = []
    
    metrics = ["accuracy", "top3_accuracy", "precision", "recall", "f1"]
    for metric in metrics:
        rows.append({
            "metric": metric,
            "flat_model": flat_results.get(metric, 0),
            "hierarchical_model": hierarchical_results.get(metric, 0),
            "improvement": hierarchical_results.get(metric, 0) - flat_results.get(metric, 0)
        })
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"\n💾 Metrics saved to: {output_path}")


def main():
    """Main evaluation function."""
    print("=" * 80)
    print("ADVANCED MODEL EVALUATION")
    print("=" * 80)
    
    # Load test data
    print("\n📊 Loading test data...")
    df_test = load_test_data()
    print(f"✅ Loaded {len(df_test)} test samples")
    
    # Evaluate flat model
    print("\n" + "=" * 80)
    print("EVALUATING FLAT MODEL")
    print("=" * 80)
    flat_results = evaluate_flat_model(df_test)
    
    if "error" not in flat_results:
        print(f"\n✅ Flat Model Results:")
        print(f"   Accuracy: {flat_results['accuracy']:.4f}")
        print(f"   Top-3 Accuracy: {flat_results['top3_accuracy']:.4f}")
        print(f"   Precision: {flat_results['precision']:.4f}")
        print(f"   Recall: {flat_results['recall']:.4f}")
        print(f"   F1-Score: {flat_results['f1']:.4f}")
    
    # Evaluate hierarchical model
    print("\n" + "=" * 80)
    print("EVALUATING HIERARCHICAL MODEL")
    print("=" * 80)
    hierarchical_results = evaluate_hierarchical_model(df_test)
    
    if "error" not in hierarchical_results:
        print(f"\n✅ Hierarchical Model Results:")
        print(f"   Accuracy: {hierarchical_results['accuracy']:.4f}")
        print(f"   Top-3 Accuracy: {hierarchical_results['top3_accuracy']:.4f}")
        print(f"   Precision: {hierarchical_results['precision']:.4f}")
        print(f"   Recall: {hierarchical_results['recall']:.4f}")
        print(f"   F1-Score: {hierarchical_results['f1']:.4f}")
    
    # Print comparison
    print_comparison(flat_results, hierarchical_results)
    
    # Save metrics
    output_path = HERE / "evaluation_metrics.csv"
    save_metrics_to_csv(flat_results, hierarchical_results, output_path)
    
    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()

