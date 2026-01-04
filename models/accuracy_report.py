# FILE: models/accuracy_report.py
import json
import os
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def generate_accuracy_report():
    """Generate a detailed accuracy report"""
    results_path = os.path.join(os.path.dirname(__file__), '..', 'evaluation_results.json')
    
    try:
        with open(results_path, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("❌ Evaluation results not found. Run 'npm run evaluate' first.")
        return
    
    print("=" * 70)
    print("📊 MODEL ACCURACY REPORT")
    print("=" * 70)
    print()
    
    for result in results:
        model_name = result['model']
        accuracy = result['accuracy']
        
        # Determine status
        if accuracy >= 0.95:
            status = "✅ Excellent"
            icon = "✅"
        elif accuracy >= 0.80:
            status = "✅ Good"
            icon = "✅"
        elif accuracy >= 0.60:
            status = "⚠️  Fair"
            icon = "⚠️"
        else:
            status = "❌ Needs Improvement"
            icon = "❌"
        
        print(f"{icon} {model_name}")
        print(f"   Accuracy: {accuracy:.2%}")
        print(f"   Status: {status}")
        
        if 'precision' in result:
            print(f"   Precision: {result['precision']:.2%}")
        if 'recall' in result:
            print(f"   Recall: {result['recall']:.2%}")
        if 'f1_score' in result:
            print(f"   F1-Score: {result['f1_score']:.2%}")
        if 'correct' in result and 'total' in result:
            print(f"   Correct: {result['correct']}/{result['total']}")
        if 'top3_accuracy' in result:
            print(f"   Top-3 Accuracy: {result['top3_accuracy']:.2%}")
        
        print()
    
    # Calculate overall
    overall = sum(r['accuracy'] for r in results) / len(results)
    print("=" * 70)
    print(f"🎯 Overall Average Accuracy: {overall:.2%}")
    
    if overall >= 0.95:
        print("🌟 Models are performing excellently!")
    elif overall >= 0.80:
        print("✅ Models are performing well!")
    else:
        print("⚠️  Consider improving models or adding more training data.")
    print("=" * 70)

if __name__ == '__main__':
    generate_accuracy_report()

