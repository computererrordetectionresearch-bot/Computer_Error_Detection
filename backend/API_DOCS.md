# PC Shop Recommendation Engine API Documentation

## 🚀 Quick Start

### Base URL
```
http://localhost:8000
```

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📋 Endpoints

### 1. Root Endpoint

**GET** `/`

Get API information and available endpoints.

**Response:**
```json
{
  "message": "PC Shop Recommendation Engine API",
  "version": "2.0.0",
  "docs": "/docs",
  "redoc": "/redoc",
  "endpoints": {
    "rank_auto": "POST /rank_auto - Get ranked shop recommendations with explainable reasons",
    "rank": "POST /rank - Manual ranking with custom candidates",
    "shop_details": "GET /shop_details - Get detailed shop information",
    "rank_products_auto": "POST /rank_products_auto - Get product recommendations",
    "tools_recommend": "GET /tools_recommend - Get tool recommendations",
    "feedback": "POST /feedback - Submit user feedback"
  },
  "status": "operational"
}
```

---

### 2. Get Ranked Shop Recommendations (Auto)

**POST** `/rank_auto`

Get ranked shop recommendations with explainable reasons. This endpoint automatically fetches shops from Supabase, builds ML features, and ranks them using the trained model.

**Request Body:**
```json
{
  "error_type": "GPU Overheat",
  "budget": "medium",
  "urgency": "high",
  "user_district": "Colombo",
  "top_k": 20
}
```

**Parameters:**
- `error_type` (string, required): Type of PC issue
  - Options: `"GPU Overheat"`, `"Blue Screen (BSOD)"`, `"Boot Failure"`, `"SSD Upgrade"`, `"RAM Upgrade"`, `"OS Installation"`, `"Laptop Screen Repair"`, `"Data Recovery"`, `"PSU / Power Issue"`, `"Wi-Fi Adapter Upgrade"`
- `budget` (string, optional): Budget level - `"low"`, `"medium"`, or `"high"` (default: `"medium"`)
- `urgency` (string, optional): Urgency level - `"normal"` or `"high"` (default: `"normal"`)
- `user_district` (string, required): User's district for location-based recommendations
- `top_k` (integer, optional): Number of top recommendations to return (1-50, default: 20)

**Response:**
```json
[
  {
    "shop_id": "shop_123",
    "shop_name": "TechFix Colombo",
    "score": 0.95,
    "shop_type": "repair_shop",
    "district": "Colombo",
    "avg_rating": 4.5,
    "reviews": 150,
    "verified": true,
    "turnaround_days": 3,
    "district_match": 1,
    "type_match": 1,
    "budget_fit": 1,
    "reason": "We recommend TechFix Colombo because it specializes in handling GPU Overheat, located in your district (Colombo), verified and trusted, excellent 4.5⭐ rating, and 150+ customer reviews.",
    "factors": [
      "Specialization match",
      "Location convenience",
      "Verified business",
      "High rating",
      "Popular choice",
      "Fast service",
      "Budget match"
    ]
  }
]
```

**Response Fields:**
- `shop_id`: Unique shop identifier
- `shop_name`: Name of the shop
- `score`: ML model prediction score (0-1, higher is better)
- `shop_type`: Type of shop (`repair_shop` or `product_shop`)
- `district`: District where the shop is located
- `avg_rating`: Average customer rating (1-5)
- `reviews`: Number of customer reviews
- `verified`: Whether the shop is verified
- `turnaround_days`: Average turnaround time in days
- `district_match`: 1 if same district as user, 0 otherwise
- `type_match`: 1 if shop type matches the error type, 0 otherwise
- `budget_fit`: 1 if budget matches, 0 otherwise
- `reason`: **Human-readable explanation** for why this shop was recommended
- `factors`: **List of key factors** that influenced the recommendation

---

### 3. Manual Ranking

**POST** `/rank`

Manual ranking with a custom candidate list. Use this when you have a pre-selected list of shops to rank.

**Request Body:**
```json
{
  "query": {
    "error_type": "GPU Overheat",
    "budget": "medium",
    "urgency": "high",
    "user_district": "Colombo",
    "top_k": 20
  },
  "candidates": [
    {
      "shop_id": "shop_123",
      "shop_type": "repair_shop",
      "district": "Colombo",
      "average_rating": 4.5,
      "reviews_count": 150,
      "verified": true,
      "average_turnaround_time": 3,
      "price_range": "medium",
      "shop_name": "TechFix Colombo"
    }
  ]
}
```

**Response:** Same as `/rank_auto`

---

### 4. Get Shop Details

**GET** `/shop_details?shop_id={shop_id}`

Get detailed information about a specific shop, including products and recent feedback.

**Parameters:**
- `shop_id` (string, required): Shop identifier

**Response:**
```json
{
  "shop": {
    "shop_id": "shop_123",
    "shop_name": "TechFix Colombo",
    "district": "Colombo",
    "average_rating": 4.5,
    "reviews_count": 150,
    "verified": true,
    "address": "123 Main Street, Colombo",
    "phone": "+94 11 123 4567",
    "email": "info@techfix.lk",
    "website": "https://techfix.lk",
    "latitude": 6.9271,
    "longitude": 79.8612
  },
  "products": [
    {
      "product_id": "prod_123",
      "brand": "Samsung",
      "model": "980 PRO",
      "category": "SSD",
      "price_lkr": 25000,
      "stock_status": "in_stock",
      "warranty": "5 years"
    }
  ],
  "feedback": [
    {
      "feedback_id": "fb_123",
      "error_type": "GPU Overheat",
      "rating": 5,
      "comment": "Excellent service!",
      "solved": true,
      "date": "2024-01-15"
    }
  ]
}
```

---

### 5. Get Product Recommendations

**POST** `/rank_products_auto`

Get product recommendations based on error type and filters.

**Request Body:**
```json
{
  "error_type": "SSD Upgrade",
  "budget": "medium",
  "urgency": "normal",
  "user_district": "Colombo",
  "top_k": 20
}
```

**Response:**
```json
[
  {
    "product_id": "prod_123",
    "brand": "Samsung",
    "model": "980 PRO",
    "category": "SSD",
    "price_lkr": 25000,
    "stock_status": "in_stock",
    "warranty": "5 years",
    "shop_id": "shop_123",
    "shop_name": "TechFix Colombo",
    "district": "Colombo",
    "avg_rating": 4.5,
    "reviews": 150,
    "verified": true,
    "match_reason": "Available at TechFix Colombo - product_shop"
  }
]
```

---

### 6. Get Tool Recommendations

**GET** `/tools_recommend?error_type={error_type}`

Get tool recommendations for specific PC issues.

**Parameters:**
- `error_type` (string, optional): Type of PC issue

**Response:**
```json
[
  {
    "tool_id": "tool_1",
    "name": "Malwarebytes",
    "category": "Antivirus",
    "os_support": ["Windows", "macOS", "Android", "iOS"],
    "license_type": "Free/Paid",
    "official_url": "https://www.malwarebytes.com/",
    "hash": "sha256:a1b2c3d4e5f6789...",
    "description": "Advanced malware protection with real-time scanning and removal capabilities.",
    "match_reason": "Highly rated antivirus with excellent detection rates"
  }
]
```

---

### 7. Submit Feedback

**POST** `/feedback`

Submit user feedback for a shop, product, or tool. This feedback is used to improve future recommendations.

**Request Body:**
```json
{
  "shop_id": "shop_123",
  "error_type": "GPU Overheat",
  "rating": 5,
  "comment": "Excellent service! Fixed my GPU overheating issue quickly.",
  "solved": true,
  "feedback_type": "shop"
}
```

**Parameters:**
- `shop_id` (string, required): Shop/product/tool identifier
- `error_type` (string, required): Type of PC issue
- `rating` (float, required): Rating from 1 to 5
- `comment` (string, optional): Additional comments
- `solved` (boolean, optional): Whether the issue was solved (default: `true`)
- `feedback_type` (string, optional): Type of feedback - `"shop"`, `"product"`, or `"tool"` (default: `"shop"`)

**Response:**
```json
{
  "message": "Feedback submitted successfully",
  "data": {
    "feedback_id": "fb_123",
    "shop_id": "shop_123",
    "rating": 5,
    "comment": "Excellent service!",
    "solved": true
  }
}
```

---

## 🔍 Explainable Reasons

The API provides **explainable reasons** for each recommendation, making it transparent why a shop was recommended. Reasons are generated based on:

1. **Specialization Match**: Shop specializes in handling the specific error type
2. **Location Convenience**: Shop is located in the user's district
3. **Verified Business**: Shop is verified and trusted
4. **High Rating**: Shop has excellent customer ratings (≥4.0)
5. **Good Rating**: Shop has good customer ratings (≥3.5)
6. **Popular Choice**: Shop has many customer reviews (≥50)
7. **Fast Service**: Shop has quick turnaround time (≤3 days for high urgency)
8. **Reasonable Turnaround**: Shop has acceptable turnaround time (≤5 days)
9. **Budget Match**: Shop matches the user's budget requirements
10. **High Quality Score**: Combination of rating, reviews, and verification

---

## 🧪 Testing

### Using cURL

```bash
# Get recommendations
curl -X POST "http://localhost:8000/rank_auto" \
  -H "Content-Type: application/json" \
  -d '{
    "error_type": "GPU Overheat",
    "budget": "medium",
    "urgency": "high",
    "user_district": "Colombo",
    "top_k": 10
  }'

# Get shop details
curl "http://localhost:8000/shop_details?shop_id=shop_123"

# Submit feedback
curl -X POST "http://localhost:8000/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "shop_id": "shop_123",
    "error_type": "GPU Overheat",
    "rating": 5,
    "comment": "Great service!",
    "solved": true
  }'
```

### Using Python

```python
import requests

# Get recommendations
response = requests.post(
    "http://localhost:8000/rank_auto",
    json={
        "error_type": "GPU Overheat",
        "budget": "medium",
        "urgency": "high",
        "user_district": "Colombo",
        "top_k": 10
    }
)
recommendations = response.json()

# Print explainable reasons
for rec in recommendations:
    print(f"\n{rec['shop_name']}:")
    print(f"  Score: {rec['score']:.2f}")
    print(f"  Reason: {rec['reason']}")
    print(f"  Factors: {', '.join(rec['factors'])}")
```

---

## 📊 Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `500 Internal Server Error`: Server error

Error responses include a `detail` field with error message:

```json
{
  "detail": "Failed to generate recommendations: Error message here"
}
```

---

## 🔐 Environment Variables

Required environment variables:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

---

## 📝 Notes

- All endpoints support CORS from `http://localhost:3000`
- The ML model uses a Random Forest classifier with 98%+ AUC
- Recommendations are ranked by ML model prediction scores
- Explainable reasons are generated dynamically based on shop features
- Feedback is stored in Supabase and used for future model training

---

## 🚀 Deployment

For production deployment:

1. Set environment variables
2. Update CORS origins in `app.py`
3. Use a production ASGI server (e.g., Gunicorn with Uvicorn workers)
4. Enable HTTPS
5. Set up monitoring and logging

Example production command:
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```




