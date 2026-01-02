// Types for the recommendation system

export interface Shop {
  shop_id: string;
  shop_name: string;
  score: number;
  shop_type: string;
  district: string;
  avg_rating?: number | null;
  reviews?: number | null;
  verified?: boolean | null;
  turnaround_days?: number | null;
  district_match: number;
  type_match: number;
  budget_fit: number;
  reason?: string;  // Explainable reason
  factors?: string[];  // Key factors
  specialization?: string[];
  open_now?: boolean;
  distance?: number;
  address?: string;
  phone?: string;
  phone_number?: string;  // Alternative phone field name
  city_address?: string;  // Full address from CSV
  website?: string;
  email?: string;
  latitude?: number;
  longitude?: number;
  google_maps_url?: string;  // Google Maps URL
}

export interface ShopDetails extends Shop {
  products?: ShopProduct[];
  recent_feedback?: ShopFeedback[];
}

export interface ShopProduct {
  product_id: string;
  brand: string;
  model: string;
  category: string;
  price_lkr: number;
  stock_status: 'in_stock' | 'low_stock' | 'out_of_stock';
}

export interface ShopFeedback {
  feedback_id: string;
  user_id?: string;
  error_type: string;
  solved: boolean;
  rating: number;
  comment?: string;
  created_at: string;
}

export interface Product {
  product_id: string;
  brand: string;
  model: string;
  category: string;
  price_lkr: number;
  stock_status: 'in_stock' | 'low_stock' | 'out_of_stock';
  warranty: string;
  shop_id: string;
  shop_name: string;
  shop_rating: number;
  shop_verified: boolean;
  specifications?: Record<string, string>;
  image_url?: string;
  detected_category?: string;  // Category detected from symptom description
  detection_confidence?: number;  // Confidence of detection (0.0-1.0)
  detection_source?: string;  // Source of detection: "rule", "ml", "ml_low_conf", or "none"
}

export interface Tool {
  tool_id: string;
  name: string;
  description: string;
  os_support: string[];
  license: 'free' | 'paid' | 'freemium' | 'open_source';
  official_url: string;
  hash?: string;
  category: string;
  error_types: string[];
}

export interface FeedbackEvent {
  chosen_id: string;
  error_type: string;
  solved: boolean;
  user_rating: number;
  feedback_type: 'shop' | 'product' | 'tool';
}

export interface SearchFilters {
  district: string;
  budget: 'low' | 'medium' | 'high' | 'custom';
  custom_budget?: number;
  urgency: 'high' | 'normal';
  verified_only: boolean;
  open_now: boolean;
}

export interface DetectionResult {
  type: 'error' | 'product' | 'tool';
  category: string;
  confidence: number;
  keywords: string[];
}

export type TabType = 'repairs' | 'products' | 'hardware';

export interface ErrorDetectionResult {
  label: string | null;
  confidence: number;
  source: string;
  alternatives: Array<{ label: string; confidence: number }>;
  similar_errors?: Array<{ label: string; confidence: number }>;
  explanation?: string | null;
  multiple_types?: Array<{ label: string; confidence: number }>;  // Multiple primary error types
}

export interface ConfirmedErrorType {
  errorType: string;
  source: 'detected' | 'user_selected';
  confidence?: number;
}

export interface BestMatch {
  shops: Shop[];
  products: Product[];
  tools: Tool[];
  summary: string;
}