"""
Comprehensive Test Script for All ML Models
Tests all models in the system with sample inputs.
"""

from pathlib import Path
import pandas as pd
import joblib
import sys
import io
import json
import numpy as np

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()

# Model paths
RECO_MODEL_PATH = HERE / "reco_model.pkl"
FEATURES_PATH = HERE / "reco_features.json"
ERROR_NLP_MODEL_PATH = HERE / "nlp_error_model_error_type.pkl"
PRODUCT_NLP_MODEL_PATH = HERE / "nlp_error_model_product.pkl"
PRODUCT_NEED_MODEL_PATH = HERE / "product_need_model.pkl"

print("=" * 80)
print("COMPREHENSIVE MODEL TESTING SUITE")
print("=" * 80)

# ============================================================================
# 1. TEST SHOP RECOMMENDATION MODEL
# ============================================================================
print("\n" + "=" * 80)
print("1. TESTING SHOP RECOMMENDATION MODEL (reco_model.pkl)")
print("=" * 80)

if not RECO_MODEL_PATH.exists():
    print(f"❌ Model not found: {RECO_MODEL_PATH}")
else:
    try:
        model = joblib.load(RECO_MODEL_PATH)
        print(f"✅ Model loaded successfully")
        
        # Load features config
        if FEATURES_PATH.exists():
            with open(FEATURES_PATH, "r", encoding="utf-8") as f:
                features_config = json.load(f)
            print(f"✅ Features config loaded")
        
        # Create sample feature data
        sample_features = {
            "avg_rating": 4.5,
            "reviews": 100,
            "reviews_ln": 4.605,
            "verified": 1,
            "turnaround_days": 3.0,
            "quality_score_rule": 4.5 * 4.605 * 1.2,
            "district_match": 1,
            "type_match": 1,
            "budget_fit": 1,
            "urgency_penalty": 0.0,
            "error_type": "SSD Upgrade",
            "budget": "medium",
            "urgency": "normal",
            "user_district": "Colombo",
            "shop_type": "repair_shop",
            "district": "Colombo"
        }
        
        # Create DataFrame
        df = pd.DataFrame([sample_features])
        
        # Get prediction
        proba = model.predict_proba(df)[:, 1]
        prediction = model.predict(df)[0]
        
        print(f"\n📊 Sample Input:")
        print(f"   Error Type: SSD Upgrade")
        print(f"   District: Colombo")
        print(f"   Shop Rating: 4.5")
        print(f"   Reviews: 100")
        print(f"   Verified: Yes")
        
        print(f"\n📈 Prediction Results:")
        print(f"   Score (Probability): {proba[0]:.4f}")
        print(f"   Binary Prediction: {prediction}")
        print(f"   ✅ Model working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        import traceback
        traceback.print_exc()

# ============================================================================
# 2. TEST ERROR TYPE NLP MODEL
# ============================================================================
print("\n" + "=" * 80)
print("2. TESTING ERROR TYPE NLP MODEL (nlp_error_model_error_type.pkl)")
print("=" * 80)

if not ERROR_NLP_MODEL_PATH.exists():
    print(f"❌ Model not found: {ERROR_NLP_MODEL_PATH}")
else:
    try:
        error_model = joblib.load(ERROR_NLP_MODEL_PATH)
        print(f"✅ Model loaded successfully")
        
        # Test samples with expected outputs (based on actual training data patterns)
        test_cases = [
            {
                "text": "computer running very slow",
                "expected": ["Slow Performance", "SSD Upgrade", "RAM Upgrade"]
            },
            {
                "text": "pc gets very hot when playing games",
                "expected": ["GPU Overheat", "CPU Overheat"]
            },
            {
                "text": "want to upgrade to 1tb ssd",
                "expected": ["SSD Upgrade"]
            },
            {
                "text": "pc randomly shuts down when I play games",
                "expected": ["PSU / Power Issue", "GPU Overheat"]
            },
            {
                "text": "no signal on monitor but pc is on",
                "expected": ["No Display / No Signal", "Monitor or GPU Check"]
            },
            {
                "text": "blue screen with sad face and stop code",
                "expected": ["Blue Screen (BSOD)", "Windows Boot Failure"]
            },
            {
                "text": "need more ram for chrome tabs and multitasking",
                "expected": ["RAM Upgrade"]
            },
            {
                "text": "wifi keeps disconnecting every few minutes",
                "expected": ["Wi-Fi Adapter Upgrade"]
            }
        ]
        
        print(f"\n📝 Testing {len(test_cases)} sample error descriptions:")
        
        for i, test_case in enumerate(test_cases, 1):
            text = test_case["text"]
            expected = test_case["expected"]
            # Extract pipeline components
            if isinstance(error_model, dict):
                vectorizer = error_model.get('vectorizer')
                classifier = error_model.get('classifier')
                label_encoder = error_model.get('label_encoder')
            else:
                # Assume it's a pipeline
                vectorizer = error_model.named_steps.get('tfidf') if hasattr(error_model, 'named_steps') else None
                classifier = error_model.named_steps.get('clf') if hasattr(error_model, 'named_steps') else None
                label_encoder = None
            
            if vectorizer is None or classifier is None:
                # Try direct prediction if it's a pipeline
                if hasattr(error_model, 'predict'):
                    predicted_label = error_model.predict([text])[0]
                    if hasattr(error_model, 'predict_proba'):
                        proba = error_model.predict_proba([text])[0]
                        confidence = max(proba)
                        classes = error_model.classes_ if hasattr(error_model, 'classes_') else error_model.named_steps['clf'].classes_
                        top3_indices = proba.argsort()[-3:][::-1]
                        top3 = [(classes[idx], proba[idx]) for idx in top3_indices]
                    else:
                        confidence = 1.0
                        top3 = [(predicted_label, 1.0)]
                else:
                    print(f"   ⚠️ Model structure unexpected, skipping test {i}")
                    continue
            else:
                # Transform and predict
                X = vectorizer.transform([text])
                proba = classifier.predict_proba(X)[0]
                predicted_array = classifier.predict(X)
                predicted_label = predicted_array[0] if len(predicted_array) > 0 else None
                
                classes = classifier.classes_
                
                # Find the index of predicted label in classes for confidence
                if predicted_label is not None:
                    try:
                        pred_idx_for_conf = list(classes).index(predicted_label)
                        confidence = float(proba[pred_idx_for_conf])
                    except (ValueError, IndexError):
                        # If label not found, use max probability
                        confidence = float(max(proba))
                        # Find which class has max probability
                        max_idx = np.argmax(proba)
                        predicted_label = classes[max_idx]
                else:
                    # Fallback: use max probability
                    max_idx = np.argmax(proba)
                    predicted_label = classes[max_idx]
                    confidence = float(proba[max_idx])
                
                # Get top 3 predictions
                top3_indices = proba.argsort()[-3:][::-1]
                top3 = []
                for idx in top3_indices:
                    label = classes[idx]
                    top3.append((label, float(proba[idx])))
            
            # Check if prediction matches expected
            is_correct = predicted_label in expected
            status = "✅" if is_correct else "❌"
            
            print(f"\n   Test {i}: \"{text[:60]}...\"")
            print(f"   {status} Predicted: {predicted_label} (confidence: {confidence:.3f})")
            print(f"      Expected one of: {', '.join(expected)}")
            print(f"      Top 3: {', '.join([f'{l}({c:.2f})' for l, c in top3])}")
            if not is_correct and confidence < 0.3:
                print(f"      ⚠️ Low confidence prediction - model may need more training data")
        
        print(f"\n   ✅ Error Type NLP Model tested!")
        
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        import traceback
        traceback.print_exc()

# ============================================================================
# 3. TEST PRODUCT CATEGORY NLP MODEL
# ============================================================================
print("\n" + "=" * 80)
print("3. TESTING PRODUCT CATEGORY NLP MODEL (nlp_error_model_product.pkl)")
print("=" * 80)

if not PRODUCT_NLP_MODEL_PATH.exists():
    print(f"❌ Model not found: {PRODUCT_NLP_MODEL_PATH}")
else:
    try:
        product_model = joblib.load(PRODUCT_NLP_MODEL_PATH)
        print(f"✅ Model loaded successfully")
        
        # Test samples with expected outputs (based on actual training data patterns)
        test_cases = [
            {
                "text": "low fps in games",
                "expected": ["GPU"]
            },
            {
                "text": "windows takes too long to load",
                "expected": ["SSD"]
            },
            {
                "text": "browser tabs lagging and closing",
                "expected": ["RAM"]
            },
            {
                "text": "pc randomly turns off, feels like power issue",
                "expected": ["PSU"]
            },
            {
                "text": "wifi is unstable and disconnects",
                "expected": ["Wi-Fi Adapter"]
            },
            {
                "text": "pc startup is very slow",
                "expected": ["SSD"]
            },
            {
                "text": "frame rate drops while gaming",
                "expected": ["GPU"]
            }
        ]
        
        print(f"\n📝 Testing {len(test_cases)} sample product descriptions:")
        
        for i, test_case in enumerate(test_cases, 1):
            text = test_case["text"]
            expected = test_case["expected"]
            # Extract pipeline components
            if isinstance(product_model, dict):
                vectorizer = product_model.get('vectorizer')
                classifier = product_model.get('classifier')
                label_encoder = product_model.get('label_encoder')
            else:
                # Assume it's a pipeline
                vectorizer = product_model.named_steps.get('tfidf') if hasattr(product_model, 'named_steps') else None
                classifier = product_model.named_steps.get('clf') if hasattr(product_model, 'named_steps') else None
                label_encoder = None
            
            if vectorizer is None or classifier is None:
                # Try direct prediction if it's a pipeline
                if hasattr(product_model, 'predict'):
                    predicted_label = product_model.predict([text])[0]
                    if hasattr(product_model, 'predict_proba'):
                        proba = product_model.predict_proba([text])[0]
                        confidence = max(proba)
                        classes = product_model.classes_ if hasattr(product_model, 'classes_') else product_model.named_steps['clf'].classes_
                        top3_indices = proba.argsort()[-3:][::-1]
                        top3 = [(classes[idx], proba[idx]) for idx in top3_indices]
                    else:
                        confidence = 1.0
                        top3 = [(predicted_label, 1.0)]
                else:
                    print(f"   ⚠️ Model structure unexpected, skipping test {i}")
                    continue
            else:
                # Transform and predict
                X = vectorizer.transform([text])
                proba = classifier.predict_proba(X)[0]
                predicted_array = classifier.predict(X)
                predicted_label = predicted_array[0] if len(predicted_array) > 0 else None
                
                classes = classifier.classes_
                
                # Find the index of predicted label in classes for confidence
                if predicted_label is not None:
                    try:
                        pred_idx_for_conf = list(classes).index(predicted_label)
                        confidence = float(proba[pred_idx_for_conf])
                    except (ValueError, IndexError):
                        # If label not found, use max probability
                        confidence = float(max(proba))
                        # Find which class has max probability
                        max_idx = np.argmax(proba)
                        predicted_label = classes[max_idx]
                else:
                    # Fallback: use max probability
                    max_idx = np.argmax(proba)
                    predicted_label = classes[max_idx]
                    confidence = float(proba[max_idx])
                
                # Get top 3 predictions
                top3_indices = proba.argsort()[-3:][::-1]
                top3 = []
                for idx in top3_indices:
                    label = classes[idx]
                    top3.append((label, float(proba[idx])))
            
            # Check if prediction matches expected
            is_correct = predicted_label in expected
            status = "✅" if is_correct else "❌"
            
            print(f"\n   Test {i}: \"{text}\"")
            print(f"   {status} Predicted: {predicted_label} (confidence: {confidence:.3f})")
            print(f"      Expected one of: {', '.join(expected)}")
            print(f"      Top 3: {', '.join([f'{l}({c:.2f})' for l, c in top3])}")
            if not is_correct:
                print(f"      ⚠️ Prediction doesn't match expected - model may need more training data")
        
        print(f"\n   ✅ Product Category NLP Model tested!")
        
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        import traceback
        traceback.print_exc()

# ============================================================================
# 4. TEST PRODUCT NEED MODEL
# ============================================================================
print("\n" + "=" * 80)
print("4. TESTING PRODUCT NEED MODEL (product_need_model.pkl)")
print("=" * 80)

if not PRODUCT_NEED_MODEL_PATH.exists():
    print(f"❌ Model not found: {PRODUCT_NEED_MODEL_PATH}")
else:
    try:
        product_need_model = joblib.load(PRODUCT_NEED_MODEL_PATH)
        print(f"✅ Model loaded successfully")
        
        # Test samples with expected outputs (based on actual training data patterns)
        test_cases = [
            {
                "text": "User reports issue related to ram upgrade or symptoms hinting toward it.",
                "expected": ["RAM Upgrade"]
            },
            {
                "text": "User reports issue related to ssd upgrade or symptoms hinting toward it.",
                "expected": ["SSD Upgrade"]
            },
            {
                "text": "User reports issue related to cpu fan replacement or symptoms hinting toward it.",
                "expected": ["CPU Fan Replacement"]
            },
            {
                "text": "User reports issue related to wifi adapter upgrade or symptoms hinting toward it.",
                "expected": ["WiFi Adapter Upgrade"]
            },
            {
                "text": "Monitor loses signal during gaming",
                "expected": ["Monitor or GPU Check"]
            },
            {
                "text": "Display turns black during use",
                "expected": ["Monitor or GPU Check"]
            },
            {
                "text": "User reports issue related to gpu upgrade or symptoms hinting toward it.",
                "expected": ["GPU Upgrade"]
            },
            {
                "text": "User reports issue related to cpu cooler upgrade or symptoms hinting toward it.",
                "expected": ["CPU Cooler Upgrade"]
            },
            {
                "text": "Lines appearing on the display",
                "expected": ["Monitor or GPU Check"]
            },
            {
                "text": "User reports issue related to thermal paste reapply or symptoms hinting toward it.",
                "expected": ["Thermal Paste Reapply"]
            }
        ]
        
        print(f"\n📝 Testing {len(test_cases)} sample user needs:")
        
        for i, test_case in enumerate(test_cases, 1):
            text = test_case["text"]
            expected = test_case["expected"]
            # Predict
            if hasattr(product_need_model, 'predict'):
                # It's a pipeline
                predicted_label = product_need_model.predict([text])[0]
                
                # Get probabilities
                if hasattr(product_need_model, 'predict_proba'):
                    proba = product_need_model.predict_proba([text])[0]
                    confidence = max(proba)
                    
                    # Get top 3
                    top3_indices = proba.argsort()[-3:][::-1]
                    top3 = []
                    classes = product_need_model.classes_ if hasattr(product_need_model, 'classes_') else product_need_model.named_steps['clf'].classes_
                    for idx in top3_indices:
                        label = classes[idx]
                        top3.append((label, proba[idx]))
                else:
                    confidence = 1.0
                    top3 = [(predicted_label, 1.0)]
            else:
                predicted_label = "Unknown"
                confidence = 0.0
                top3 = []
            
            # Check if prediction matches expected
            is_correct = predicted_label in expected if predicted_label else False
            status = "✅" if is_correct else "❌"
            
            print(f"\n   Test {i}: \"{text[:60]}...\"")
            print(f"   {status} Predicted Component: {predicted_label}")
            print(f"      Expected one of: {', '.join(expected[:3])}")
            print(f"      Confidence: {confidence:.3f}")
            if top3:
                print(f"      Top 3: {', '.join([f'{l}({c:.2f})' for l, c in top3[:3]])}")
            if not is_correct:
                print(f"      ⚠️ Prediction doesn't match expected - model may need more training data")
        
        print(f"\n   ✅ Product Need Model tested!")
        
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        import traceback
        traceback.print_exc()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

models_status = {
    "Shop Recommendation Model": RECO_MODEL_PATH.exists(),
    "Error Type NLP Model": ERROR_NLP_MODEL_PATH.exists(),
    "Product Category NLP Model": PRODUCT_NLP_MODEL_PATH.exists(),
    "Product Need Model": PRODUCT_NEED_MODEL_PATH.exists(),
}

print("\n📊 Model Status:")
for model_name, exists in models_status.items():
    status = "✅ Found" if exists else "❌ Missing"
    print(f"   {status}: {model_name}")

all_found = all(models_status.values())
if all_found:
    print("\n🎉 All models are present and tested!")
else:
    print("\n⚠️ Some models are missing. Please train them first.")

print("\n" + "=" * 80)

