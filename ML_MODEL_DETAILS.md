# Machine Learning Model - Complete Documentation

## Table of Contents
1. [Model Overview](#model-overview)
2. [How It Works](#how-it-works)
3. [Model Architecture](#model-architecture)
4. [Training Process](#training-process)
5. [Using the Model](#using-the-model)
6. [API Reference](#api-reference)
7. [Data Structure](#data-structure)
8. [Performance Metrics](#performance-metrics)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Model Overview

### What is This Model?
This is a **semantic similarity-based error detection system** that uses advanced Natural Language Processing (NLP) to match user-described computer errors with solutions from a comprehensive database.

### Key Features
- **Semantic Understanding**: Understands meaning, not just keywords
- **High Accuracy**: 80-90% confidence for well-described errors
- **Fast Inference**: < 100ms per query
- **Comprehensive Coverage**: 1,329+ unique error scenarios
- **Context-Aware**: Considers symptoms, causes, and error descriptions

### Technology Stack
- **Model**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **Framework**: FastAPI (Python)
- **Frontend**: Next.js 14 (React/TypeScript)
- **Embeddings**: 384-dimensional vectors
- **Similarity Metric**: Cosine similarity

---

## How It Works

### 1. Training Phase

```
CSV Datasets → Data Processing → Text Embeddings → Model Storage
```

**Step-by-Step:**
1. Load CSV files from `Datasets/` folder
2. Combine and deduplicate error records
3. Create text representations: `user_error_text + symptoms + error_name`
4. Generate embeddings using Sentence Transformer
5. Save embeddings and model to disk

### 2. Inference Phase

```
User Input → Embedding → Similarity Search → Best Match → Solution
```

**Step-by-Step:**
1. User enters error description
2. Convert to 384-dim embedding vector
3. Calculate cosine similarity with all stored embeddings
4. Find highest similarity match
5. Return solution with confidence score

### 3. Semantic Matching Example

**User Input:** "My computer screen is black when I turn it on"

**Matches:**
- ✅ "Black screen on boot" (85% confidence)
- ✅ "System fails to boot to Windows" (82% confidence)
- ❌ "No audio output" (15% confidence)

The model understands that "black screen" and "screen is black" mean the same thing!

---

## Model Architecture

### Sentence Transformer Model

**Model Name:** `all-MiniLM-L6-v2`

**Specifications:**
- **Type**: BERT-based transformer
- **Parameters**: ~22.7M
- **Embedding Dimension**: 384
- **Max Sequence Length**: 256 tokens
- **Language**: English (multilingual support available)
- **Size**: ~80MB

**Why This Model?**
- ✅ Fast inference (< 100ms)
- ✅ Good accuracy for semantic similarity
- ✅ Pre-trained on millions of text pairs
- ✅ Optimized for production use
- ✅ Low memory footprint

### Embedding Process

```python
# Pseudo-code
text = "I get Black screen on boot when using my PC"
embedding = model.encode(text)  # Returns 384-dim vector
# embedding shape: (384,)
```

### Similarity Calculation

```python
# Cosine similarity formula
similarity = dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))
# Returns value between -1 and 1 (typically 0 to 1 for similar texts)
```

---

## Training Process

### Data Sources

**Primary Datasets:**
- `IT22002792_AllCategories_V2_1000.csv` - 1,000 comprehensive errors
- `IT22002792_ERRORCODES_2000.csv` - 2,000 error codes

**Training Datasets:**
- Audio, Boot, BSOD, Display, Driver, Hardware, Network, Performance, Storage, Windows Update
- Each with 100 training examples

**Total Records:** ~3,990 (before deduplication)
**Unique Errors:** 1,329 (after deduplication)

### Training Command

```bash
cd ml_backend
python train_model.py
```

### What Happens During Training

1. **Data Loading** (30 seconds)
   - Reads all CSV files
   - Combines datasets
   - Removes duplicates

2. **Data Preparation** (10 seconds)
   - Creates combined text representations
   - Formats solution steps with titles
   - Validates data quality

3. **Model Download** (First time only, 2-5 minutes)
   - Downloads pre-trained model from Hugging Face
   - ~80MB download

4. **Embedding Generation** (30-60 seconds)
   - Creates embeddings for all 1,329 errors
   - Batch processing (32 errors per batch)
   - Progress bar shows completion

5. **Model Saving** (10 seconds)
   - Saves transformer model
   - Saves error database
   - Saves embeddings as numpy array

**Total Time:** ~2-3 minutes (after first download)

### Output Files

```
ml_backend/models/
├── sentence_transformer/     # Saved model
│   ├── config.json
│   ├── model.safetensors
│   └── tokenizer files
├── error_database_no_emb.pkl # Error data (without embeddings)
├── error_database.pkl        # Error data (with embeddings)
└── embeddings.npy           # Pre-computed embeddings (384 x 1329)
```

---

## Using the Model

### Method 1: Web Interface

1. Start backend: `cd ml_backend && python app.py`
2. Start frontend: `npm run dev`
3. Open: `http://localhost:3000`
4. Enter error description
5. Click "Detect Error & Generate Solution"

### Method 2: API Direct

**Endpoint:** `POST http://localhost:8000/detect-error`

**Request:**
```json
{
  "user_error": "I get Black screen on boot when using my PC"
}
```

**Response:**
```json
{
  "error_name": "Black screen on boot",
  "category": "Boot & Startup",
  "confidence": 0.83,
  "steps": [
    "Step 1: Basic Checks (Very Important)\n\n1. Check BIOS/UEFI boot order...",
    "Step 2: Check If Windows Is Actually Booting\n\n1. Turn on PC...",
    ...
  ],
  "symptoms": "System fails to boot to Windows...",
  "cause": "Bootloader corruption, disk errors...",
  "risk": "medium",
  "verification": "Confirm the system behaves normally..."
}
```

### Method 3: Python Script

```python
import requests

response = requests.post(
    'http://localhost:8000/detect-error',
    json={'user_error': 'No audio output from speakers'}
)

result = response.json()
print(f"Error: {result['error_name']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Steps: {len(result['steps'])}")
```

### Method 4: Command Line (curl)

```bash
curl -X POST http://localhost:8000/detect-error \
  -H "Content-Type: application/json" \
  -d '{"user_error": "High CPU usage making my computer slow"}'
```

---

## API Reference

### POST `/detect-error`

Detect error and get solution.

**Request Body:**
```json
{
  "user_error": "string (required)"
}
```

**Response:**
```json
{
  "error_name": "string",
  "category": "string",
  "confidence": 0.0-1.0,
  "steps": ["string"],
  "symptoms": "string",
  "cause": "string",
  "risk": "low|medium|high",
  "verification": "string"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request (missing user_error)
- `404`: No matching error found
- `500`: Server error
- `503`: Model not loaded

### GET `/health`

Check API health and model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "database_size": 1329
}
```

### GET `/search-errors`

Search for multiple similar errors.

**Query Parameters:**
- `query`: Search text (required)
- `limit`: Number of results (default: 5)

**Example:**
```
GET /search-errors?query=black%20screen&limit=3
```

---

## Data Structure

### Error Database Schema

Each error record contains:

```python
{
    'id': 'ALLV2-0126',
    'error_name': 'Black screen on boot',
    'category': 'Boot & Startup',
    'user_error_text': 'I get Black screen on boot when using my PC',
    'symptoms': 'System fails to boot to Windows; error messages...',
    'cause': 'Bootloader corruption, disk errors, or incorrect BIOS settings.',
    'solution_steps': [
        'Step 1: Basic Checks (Very Important)\n\n1. Check BIOS...',
        'Step 2: Check If Windows Is Actually Booting\n\n1. Turn on PC...',
        ...
    ],
    'verification': 'Confirm the system behaves normally...',
    'risk': 'medium',
    'os_version': 'Windows 10',
    'device_type': 'All-in-One',
    'tag': 'Boot'
}
```

### Solution Steps Format

Each step is formatted as:
```
Step X: Title

1. Sub-step one
2. Sub-step two
3. Sub-step three
```

**Example:**
```
Step 1: Basic Checks (Very Important)

1. Check BIOS/UEFI boot order and ensure correct drive is selected
2. Disconnect external devices and try booting again
```

### Categories

- Boot & Startup
- Display / Graphics
- Audio / Microphone
- Network / Internet
- Storage & Disk
- Performance & Slow PC
- Driver & Device
- Windows Update / OS
- BSOD (Blue Screen of Death)
- Hardware Failure
- Security, Virus & Permission
- Application & Software Error Codes

---

## Performance Metrics

### Accuracy

**Confidence Score Interpretation:**
- **> 0.80 (80%)**: Excellent match - Very likely correct
- **0.60 - 0.80 (60-80%)**: Good match - Probably correct
- **0.40 - 0.60 (40-60%)**: Moderate match - May need verification
- **< 0.40 (40%)**: Poor match - May not be relevant

**Typical Performance:**
- Well-described errors: 80-90% confidence
- Vague descriptions: 60-70% confidence
- Unrelated queries: < 40% confidence

### Speed

- **Model Loading**: ~5-10 seconds (first time)
- **Inference Time**: < 100ms per query
- **API Response**: < 200ms (including network)
- **Database Size**: 1,329 errors
- **Embedding Dimension**: 384

### Scalability

- **Concurrent Requests**: 100+ (limited by server resources)
- **Database Search**: O(n) where n = number of errors
- **Memory Usage**: ~500MB (model + embeddings)
- **CPU Usage**: Low (GPU optional, not required)

---

## Best Practices

### For Users

1. **Be Descriptive**
   - ✅ Good: "I get Black screen on boot when using my PC"
   - ❌ Bad: "Black screen"

2. **Include Context**
   - ✅ Good: "No audio output from my speakers after Windows update"
   - ❌ Bad: "No sound"

3. **Use Natural Language**
   - ✅ Good: "My computer is running very slowly"
   - ❌ Bad: "CPU error code 0x00000000"

4. **Mention When It Happens**
   - ✅ Good: "High CPU usage making my computer slow during startup"
   - ❌ Bad: "CPU problem"

### For Developers

1. **Error Handling**
   ```python
   try:
       response = requests.post(url, json=data)
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       # Handle error
   ```

2. **Timeout Settings**
   ```python
   response = requests.post(url, json=data, timeout=5)
   ```

3. **Retry Logic**
   ```python
   for attempt in range(3):
       try:
           response = requests.post(url, json=data)
           break
       except:
           if attempt == 2:
               raise
           time.sleep(1)
   ```

4. **Caching** (Optional)
   - Cache frequent queries
   - Use Redis or in-memory cache
   - TTL: 1 hour recommended

---

## Troubleshooting

### Model Not Loading

**Error:** "Model not loaded. Please train the model first."

**Solution:**
```bash
cd ml_backend
python train_model.py
```

**Check:**
- `ml_backend/models/` folder exists
- `error_database_no_emb.pkl` exists
- `embeddings.npy` exists
- `sentence_transformer/` folder exists

### Low Confidence Scores

**Problem:** Getting < 50% confidence for valid errors

**Solutions:**
1. **Improve user input**: Ask for more details
2. **Retrain with more data**: Add similar errors to dataset
3. **Check data quality**: Ensure CSV files are properly formatted

### Slow Performance

**Problem:** Queries taking > 1 second

**Solutions:**
1. **Check server resources**: CPU/RAM usage
2. **Reduce database size**: Remove unused errors
3. **Use GPU**: Install CUDA-enabled PyTorch
4. **Optimize embeddings**: Use smaller model (trade-off accuracy)

### Memory Issues

**Problem:** Out of memory errors

**Solutions:**
1. **Reduce batch size**: In `train_model.py`, change `batch_size=32` to `16`
2. **Use CPU-only**: Install CPU-only PyTorch
3. **Increase system RAM**: Recommended 4GB+ for model

### API Connection Errors

**Problem:** "Failed to connect to ML backend"

**Solutions:**
1. **Check backend is running**: `http://localhost:8000/health`
2. **Check port**: Ensure port 8000 is not in use
3. **Check firewall**: Allow port 8000
4. **Check CORS**: Backend allows all origins by default

---

## Advanced Usage

### Custom Model Training

To use a different model:

```python
# In train_model.py
# Change from:
model = SentenceTransformer('all-MiniLM-L6-v2')

# To (better accuracy, slower):
model = SentenceTransformer('all-mpnet-base-v2')

# Or (faster, less accurate):
model = SentenceTransformer('all-MiniLM-L12-v2')
```

### Fine-Tuning

To fine-tune on your own data:

```python
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare your training data
train_examples = [
    InputExample(texts=['User error 1', 'Matched error 1'], label=1.0),
    InputExample(texts=['User error 2', 'Matched error 2'], label=0.9),
    # ... more examples
]

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)

# Fine-tune
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3,
    output_path='./fine-tuned-model'
)
```

### Batch Processing

Process multiple errors at once:

```python
import requests

errors = [
    "Black screen on boot",
    "No audio output",
    "High CPU usage"
]

results = []
for error in errors:
    response = requests.post(
        'http://localhost:8000/detect-error',
        json={'user_error': error}
    )
    results.append(response.json())
```

### Export Results

Save results to file:

```python
import json
import requests

response = requests.post(
    'http://localhost:8000/detect-error',
    json={'user_error': 'Your error here'}
)

with open('result.json', 'w') as f:
    json.dump(response.json(), f, indent=2)
```

---

## Model Limitations

1. **Language**: Optimized for English (works with other languages but accuracy may vary)
2. **Domain**: Computer/Windows errors only
3. **Accuracy**: Depends on how well user describes the error
4. **Coverage**: Only matches errors in the training database
5. **Context**: Doesn't consider system-specific details (hardware model, etc.)

---

## Future Improvements

1. **Multi-language Support**: Train on translated datasets
2. **Context Awareness**: Consider OS version, hardware specs
3. **Learning from Feedback**: Update model based on user corrections
4. **Conversational Interface**: Multi-turn dialogue for better diagnosis
5. **Image Support**: Analyze screenshots of errors
6. **Real-time Updates**: Add new errors without retraining

---

## Support & Resources

- **Model Documentation**: https://www.sbert.net/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Sentence Transformers**: https://huggingface.co/sentence-transformers
- **Dataset Format**: See `Datasets/` folder for CSV structure

---

## Version Information

- **Model Version**: all-MiniLM-L6-v2
- **API Version**: 1.0.0
- **Database Version**: 1.0 (1,329 errors)
- **Last Updated**: 2024




















