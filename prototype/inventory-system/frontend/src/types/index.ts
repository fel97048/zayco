export interface User {
  id: number;
  username: string;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  created_at: string;
}

export interface Product {
  id: number;
  name: string;
  category_id: number;
  category: Category;
  barcode?: string;
  unit: string;
  created_at: string;
}

export interface Inventory {
  id: number;
  product_id: number;
  product: Product;
  quantity: number;
  expiry_date?: string;
  updated_at: string;
}

export interface InventoryHistory {
  id: number;
  product_id: number;
  user_id: number;
  transaction_type: string;
  quantity: number;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface ProductCreate {
  name: string;
  category_id: number;
  barcode?: string;
  unit: string;
}

export interface CategoryCreate {
  name: string;
}

export interface InventoryTransaction {
  product_id: number;
  transaction_type: '購入' | '使用';
  quantity: number;
}
