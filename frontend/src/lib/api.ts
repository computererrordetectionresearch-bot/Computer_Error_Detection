// API utility functions for the recommendation system

const API_BASE_URL = process.env.NEXT_PUBLIC_RECO_API_URL || "http://localhost:8000";

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

// Repair/Shop related API calls
export const searchRepairs = async (params: {
  error_type: string;
  budget: string;
  urgency: string;
  user_district: string;
}) => {
  const response = await fetch(`${API_BASE_URL}/rank_auto`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch repairs');
  }
  
  return response.json();
};

export const getShopDetails = async (shopId: string) => {
  const response = await fetch(`${API_BASE_URL}/shop_details?shop_id=${shopId}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch shop details');
  }
  
  return response.json();
};

// Product related API calls
export const searchProductsAuto = async (params: {
  product_type: string;
  budget: string;
  district: string;
}) => {
  const response = await fetch(`${API_BASE_URL}/rank_products_auto`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }
  
  return response.json();
};

export const searchProductsByQuery = async (params: {
  query: string;
  budget: string;
  district: string;
}) => {
  const response = await fetch(`${API_BASE_URL}/rank_products_by_query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }
  
  return response.json();
};

export const getProductDetails = async (productId: string) => {
  const response = await fetch(`${API_BASE_URL}/product_details?product_id=${productId}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch product details');
  }
  
  return response.json();
};

// Tool related API calls
export const getToolsRecommendation = async (errorType: string) => {
  const response = await fetch(`${API_BASE_URL}/tools_recommend?error_type=${errorType}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch tools');
  }
  
  return response.json();
};

export const getToolDetails = async (toolId: string) => {
  const response = await fetch(`${API_BASE_URL}/tool_details?tool_id=${toolId}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch tool details');
  }
  
  return response.json();
};

// Feedback API call
export const submitFeedback = async (feedback: {
  chosen_id: string;
  error_type: string;
  solved: boolean;
  user_rating: number;
  feedback_type: 'shop' | 'product' | 'tool';
}) => {
  const response = await fetch(`${API_BASE_URL}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(feedback)
  });
  
  if (!response.ok) {
    throw new Error('Failed to submit feedback');
  }
  
  return response.json();
};