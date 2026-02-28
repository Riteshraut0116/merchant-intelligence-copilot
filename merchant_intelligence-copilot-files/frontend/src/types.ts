export interface Product {
  product_name: string;
  confidence_score: number;
  reorder?: {
    quantity: number;
    urgency: string;
  };
  anomalies?: Array<{
    type: string;
    severity: string;
  }>;
  forecast?: Array<{
    ds: string;
    yhat: number;
    yhat_lower?: number;
    yhat_upper?: number;
  }>;
  demand_reasoning?: string;
  reorder_logic?: string;
  confidence_explanation?: string;
}

export interface InsightsData {
  summary: string;
  insights?: {
    products: Product[];
  };
  products?: Product[];
  forecast?: Array<{
    ds: string;
    yhat: number;
    yhat_lower?: number;
    yhat_upper?: number;
  }>;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  confidence?: number;
  timestamp: number;
}
