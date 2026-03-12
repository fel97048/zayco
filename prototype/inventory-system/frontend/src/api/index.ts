import axios from 'axios';
import type {
  User,
  Category,
  Product,
  Inventory,
  InventoryHistory,
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  ProductCreate,
  CategoryCreate,
  InventoryTransaction,
} from '@/types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// リクエストインターセプター：トークンを自動付与
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 認証API
export const authApi = {
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const response = await api.post<TokenResponse>('/api/users/login', data);
    return response.data;
  },
  register: async (data: RegisterRequest): Promise<User> => {
    const response = await api.post<User>('/api/users/register', data);
    return response.data;
  },
  getMe: async (): Promise<User> => {
    const response = await api.get<User>('/api/users/me');
    return response.data;
  },
};

// カテゴリAPI
export const categoryApi = {
  getAll: async (): Promise<Category[]> => {
    const response = await api.get<Category[]>('/api/categories');
    return response.data;
  },
  create: async (data: CategoryCreate): Promise<Category> => {
    const response = await api.post<Category>('/api/categories', data);
    return response.data;
  },
};

// 商品API
export const productApi = {
  getAll: async (): Promise<Product[]> => {
    const response = await api.get<Product[]>('/api/products');
    return response.data;
  },
  create: async (data: ProductCreate): Promise<Product> => {
    const response = await api.post<Product>('/api/products', data);
    return response.data;
  },
  update: async (id: number, data: Partial<ProductCreate>): Promise<Product> => {
    const response = await api.put<Product>(`/api/products/${id}`, data);
    return response.data;
  },
  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/products/${id}`);
  },
};

// 在庫API
export const inventoryApi = {
  getAll: async (): Promise<Inventory[]> => {
    const response = await api.get<Inventory[]>('/api/inventory');
    return response.data;
  },
  transaction: async (data: InventoryTransaction): Promise<InventoryHistory> => {
    const response = await api.post<InventoryHistory>('/api/inventory/transaction', data);
    return response.data;
  },
  getHistory: async (): Promise<InventoryHistory[]> => {
    const response = await api.get<InventoryHistory[]>('/api/inventory/history');
    return response.data;
  },
};

export default api;
