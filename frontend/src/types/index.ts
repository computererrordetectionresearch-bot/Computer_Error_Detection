// Shop Recommendation Types
export interface ShopRecommendation {
  shop_id: string;
  shop_name: string;
  score: number;
  shop_type: string;
  district: string;
  avg_rating: number;
  reviews: number;
  verified: number;
  turnaround_days: number;
  district_match: number;
  type_match: number;
  budget_fit: number;
  specialization?: string;
  is_open?: boolean;
  distance?: number;
}

// Product Recommendation Types
export interface ProductRecommendation {
  product_id: string;
  brand: string;
  model: string;
  category: string;
  price_lkr: number;
  stock_status: string;
  warranty: string;
  shop_id: string;
  shop_name: string;
  district: string;
  avg_rating: number;
  reviews: number;
  verified: number;
  match_reason?: string;
}

// Tool Recommendation Types
export interface ToolRecommendation {
  tool_id: string;
  name: string;
  category: string;
  os_support: string[];
  license_type: string;
  official_url: string;
  hash?: string;
  description: string;
  match_reason?: string;
}

// Feedback Types
export interface FeedbackEvent {
  chosen_id: string;
  error_type: string;
  solved: boolean;
  user_rating: number;
  comment?: string;
}

// Form Data Types
export interface SearchFormData {
  query: string;
  district: string;
  budget: string;
  urgency: string;
  verified_only: boolean;
  open_now: boolean;
}

// API Response Types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

// Detection Types
export interface DetectionResult {
  type: 'repair' | 'product' | 'tool';
  category: string;
  confidence: number;
  extracted_info?: {
    budget?: number;
    urgency?: string;
    specifications?: string[];
  };
}
