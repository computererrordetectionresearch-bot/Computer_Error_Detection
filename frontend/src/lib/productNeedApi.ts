"use client";

export interface ProductNeedAlternative {
  label: string;
  confidence: number;
}

export interface ProductNeedResponse {
  component: string | null;
  need_label: string | null;
  confidence: number;
  definition: string | null;
  why_useful: string | null;
  extra_explanation: string | null;
  alternatives: ProductNeedAlternative[];
  fixing_tips?: string[] | null;
}

const API_BASE_URL =
  process.env.NEXT_PUBLIC_RECO_API_URL || "http://localhost:8000";

export async function fetchProductNeedRecommend(params: {
  text: string;
  budget?: string;
  district?: string;
  user_district?: string;
}): Promise<ProductNeedResponse> {
  const body = {
    text: params.text,
    budget: params.budget ?? "medium",
    district: params.district ?? "",
    user_district: params.user_district ?? params.district ?? "",
  };

  const res = await fetch(`${API_BASE_URL}/product_need_recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(
      `Failed to fetch product_need_recommend: ${res.status} ${res.statusText}`,
    );
  }

  return res.json();
}

