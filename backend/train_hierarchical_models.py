"""
Train hierarchical Product Need Models:
1. Category Model (5 classes: Performance, Power, Network, Display, Storage)
2. Component Model (48 classes, filtered by category)

Uses TF-IDF with both word n-grams (1-2) and character n-grams (3-5).
"""

from pathlib import Path
import pandas as pd
import joblib
import json
import sys
import io
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()
MAPPING_PATH = HERE / "component_category_mapping.json"

# Model paths
CATEGORY_MODEL_PATH = HERE / "product_need_category_model.pkl"
COMPONENT_MODEL_PATH = HERE / "product_need_component_model.pkl"

print("=" * 80)
print("HIERARCHICAL PRODUCT NEED MODEL TRAINING")
print("=" * 80)

# Load component-to-category mapping
if not MAPPING_PATH.exists():
    print(f"❌ Mapping file not found: {MAPPING_PATH}")
    sys.exit(1)

with open(MAPPING_PATH, 'r', encoding='utf-8') as f:
    category_mapping = json.load(f)

# Create reverse mapping: component -> category
component_to_category = {}
for category, components in category_mapping.items():
    for component in components:
        component_to_category[component] = category

print(f"✅ Loaded mapping: {len(component_to_category)} components → 5 categories")

# Load training data
HARDWARE_CSV = DATA_DIR / "hardware_component_dataset_merged.csv"
if not HARDWARE_CSV.exists():
    print(f"❌ Training data not found: {HARDWARE_CSV}")
    sys.exit(1)

df = pd.read_csv(HARDWARE_CSV)
df = df.dropna(subset=['user_text', 'component_label'])
df['text'] = df['user_text'].astype(str).str.lower().str.strip()
df = df[df['text'].str.len() > 0]

# Map components to categories
df['category'] = df['component_label'].map(component_to_category)
df = df.dropna(subset=['category'])

print(f"📊 Loaded {len(df)} training samples")
print(f"📊 Categories: {df['category'].nunique()}")
print(f"📊 Components: {df['component_label'].nunique()}")

# Category distribution
print(f"\nCategory distribution:")
print(df['category'].value_counts())

# ============================================================================
# TRAIN CATEGORY MODEL (Stage 1)
# ============================================================================
print("\n" + "=" * 80)
print("STAGE 1: TRAINING CATEGORY MODEL")
print("=" * 80)

X_category = df['text'].values
y_category = df['category'].values

# Split data
try:
    X_cat_train, X_cat_test, y_cat_train, y_cat_test = train_test_split(
        X_category, y_category, test_size=0.2, random_state=42, stratify=y_category
    )
except:
    X_cat_train, X_cat_test, y_cat_train, y_cat_test = train_test_split(
        X_category, y_category, test_size=0.2, random_state=42
    )

print(f"📊 Train: {len(X_cat_train)}, Test: {len(X_cat_test)}")

# Create TF-IDF with word and character n-grams
word_tfidf = TfidfVectorizer(
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    stop_words='english',
    analyzer='word'
)

char_tfidf = TfidfVectorizer(
    ngram_range=(3, 5),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    analyzer='char'
)

# Combine features
feature_union = FeatureUnion([
    ('word_tfidf', word_tfidf),
    ('char_tfidf', char_tfidf)
])

# Test algorithms
algorithms = {
    'LogisticRegression': LogisticRegression(max_iter=500, random_state=42, C=1.0, multi_class='multinomial'),
    'SGDClassifier': SGDClassifier(random_state=42, max_iter=1000, loss='log_loss'),
    'MultinomialNB': MultinomialNB(alpha=0.5),
}

best_score = 0
best_model = None
best_name = None

print("\n🔍 Testing different algorithms...")
for name, clf in algorithms.items():
    pipeline = Pipeline([
        ('features', feature_union),
        ('clf', clf)
    ])
    
    try:
        scores = cross_val_score(pipeline, X_cat_train, y_cat_train, cv=3, scoring='accuracy')
        avg_score = scores.mean()
        
        print(f"   {name:20s}: {avg_score:.4f} (+/- {scores.std():.4f})")
        
        if avg_score > best_score:
            best_score = avg_score
            best_model = pipeline
            best_name = name
    except Exception as e:
        print(f"   {name:20s}: Failed ({str(e)[:50]})")

if best_model is None:
    print("❌ All algorithms failed. Using default LogisticRegression.")
    best_model = Pipeline([
        ('features', feature_union),
        ('clf', LogisticRegression(max_iter=500, random_state=42, multi_class='multinomial'))
    ])
    best_name = "LogisticRegression (default)"

print(f"\n✅ Best algorithm: {best_name} (CV Score: {best_score:.4f})")

# Train best model
print("\n🔄 Training category model...")
best_model.fit(X_cat_train, y_cat_train)

# Evaluate
y_cat_pred = best_model.predict(X_cat_test)
cat_accuracy = accuracy_score(y_cat_test, y_cat_pred)

print(f"\n📈 Category Model Test Accuracy: {cat_accuracy:.4f}")
print(f"\n📊 Classification Report:")
print(classification_report(y_cat_test, y_cat_pred))

# Save category model
joblib.dump(best_model, CATEGORY_MODEL_PATH)
print(f"\n💾 Category model saved to: {CATEGORY_MODEL_PATH}")

# ============================================================================
# TRAIN COMPONENT MODEL (Stage 2)
# ============================================================================
print("\n" + "=" * 80)
print("STAGE 2: TRAINING COMPONENT MODEL")
print("=" * 80)

X_component = df['text'].values
y_component = df['component_label'].values

# Filter classes with at least 2 samples
class_counts = pd.Series(y_component).value_counts()
valid_classes = class_counts[class_counts >= 2].index
df_filtered = df[df['component_label'].isin(valid_classes)]

if len(df_filtered) < len(df) * 0.8:
    print(f"\n⚠️ Filtered out {len(df) - len(df_filtered)} samples with rare classes")
    print(f"   Using {len(df_filtered)} samples for training")
    X_component = df_filtered['text'].values
    y_component = df_filtered['component_label'].values

# Split data
try:
    X_comp_train, X_comp_test, y_comp_train, y_comp_test = train_test_split(
        X_component, y_component, test_size=0.2, random_state=42, stratify=y_component
    )
except:
    X_comp_train, X_comp_test, y_comp_train, y_comp_test = train_test_split(
        X_component, y_component, test_size=0.2, random_state=42
    )

print(f"📊 Train: {len(X_comp_train)}, Test: {len(X_comp_test)}")

# Use same feature union
feature_union_comp = FeatureUnion([
    ('word_tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95, sublinear_tf=True, stop_words='english', analyzer='word')),
    ('char_tfidf', TfidfVectorizer(ngram_range=(3, 5), min_df=2, max_df=0.95, sublinear_tf=True, analyzer='char'))
])

# Test algorithms
best_score_comp = 0
best_model_comp = None
best_name_comp = None

print("\n🔍 Testing different algorithms...")
for name, clf in algorithms.items():
    pipeline = Pipeline([
        ('features', feature_union_comp),
        ('clf', clf)
    ])
    
    try:
        scores = cross_val_score(pipeline, X_comp_train, y_comp_train, cv=3, scoring='accuracy')
        avg_score = scores.mean()
        
        print(f"   {name:20s}: {avg_score:.4f} (+/- {scores.std():.4f})")
        
        if avg_score > best_score_comp:
            best_score_comp = avg_score
            best_model_comp = pipeline
            best_name_comp = name
    except Exception as e:
        print(f"   {name:20s}: Failed ({str(e)[:50]})")

if best_model_comp is None:
    print("❌ All algorithms failed. Using default LogisticRegression.")
    best_model_comp = Pipeline([
        ('features', feature_union_comp),
        ('clf', LogisticRegression(max_iter=500, random_state=42, multi_class='multinomial'))
    ])
    best_name_comp = "LogisticRegression (default)"

print(f"\n✅ Best algorithm: {best_name_comp} (CV Score: {best_score_comp:.4f})")

# Train best model
print("\n🔄 Training component model...")
best_model_comp.fit(X_comp_train, y_comp_train)

# Evaluate
y_comp_pred = best_model_comp.predict(X_comp_test)
comp_accuracy = accuracy_score(y_comp_test, y_comp_pred)

print(f"\n📈 Component Model Test Accuracy: {comp_accuracy:.4f}")
print(f"\n📊 Top 10 classes classification report:")
top_classes = pd.Series(y_comp_test).value_counts().head(10).index
top_mask = np.isin(y_comp_test, top_classes)
if top_mask.sum() > 0:
    print(classification_report(y_comp_test[top_mask], y_comp_pred[top_mask]))

# Save component model
joblib.dump(best_model_comp, COMPONENT_MODEL_PATH)
print(f"\n💾 Component model saved to: {COMPONENT_MODEL_PATH}")

# Save mapping for inference
MAPPING_SAVE_PATH = HERE / "component_category_mapping.json"
with open(MAPPING_SAVE_PATH, 'w', encoding='utf-8') as f:
    json.dump(category_mapping, f, indent=2, ensure_ascii=False)

print(f"\n💾 Component-to-category mapping saved to: {MAPPING_SAVE_PATH}")

print("\n" + "=" * 80)
print("TRAINING COMPLETE")
print("=" * 80)
print(f"✅ Category Model: {cat_accuracy:.4f} accuracy")
print(f"✅ Component Model: {comp_accuracy:.4f} accuracy")
print(f"✅ Models ready for hierarchical inference!")

