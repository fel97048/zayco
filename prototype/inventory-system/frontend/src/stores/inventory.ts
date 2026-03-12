import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Category, Product, Inventory, InventoryHistory } from '@/types';
import { categoryApi, productApi, inventoryApi } from '@/api';

export const useInventoryStore = defineStore('inventory', () => {
  const categories = ref<Category[]>([]);
  const products = ref<Product[]>([]);
  const inventory = ref<Inventory[]>([]);
  const history = ref<InventoryHistory[]>([]);

  const fetchCategories = async () => {
    categories.value = await categoryApi.getAll();
  };

  const createCategory = async (name: string) => {
    const newCategory = await categoryApi.create({ name });
    categories.value.push(newCategory);
    return newCategory;
  };

  const fetchProducts = async () => {
    products.value = await productApi.getAll();
  };

  const createProduct = async (data: {
    name: string;
    category_id: number;
    barcode?: string;
    unit: string;
  }) => {
    const newProduct = await productApi.create(data);
    products.value.push(newProduct);
    await fetchInventory();
    return newProduct;
  };

  const updateProduct = async (id: number, data: Partial<{
    name: string;
    category_id: number;
    barcode?: string;
    unit: string;
  }>) => {
    const updated = await productApi.update(id, data);
    const index = products.value.findIndex((p) => p.id === id);
    if (index !== -1) {
      products.value[index] = updated;
    }
    return updated;
  };

  const deleteProduct = async (id: number) => {
    await productApi.delete(id);
    products.value = products.value.filter((p) => p.id !== id);
    inventory.value = inventory.value.filter((i) => i.product_id !== id);
  };

  const fetchInventory = async () => {
    inventory.value = await inventoryApi.getAll();
  };

  const addTransaction = async (data: {
    product_id: number;
    transaction_type: '購入' | '使用';
    quantity: number;
  }) => {
    const newHistory = await inventoryApi.transaction(data);
    await fetchInventory();
    history.value.unshift(newHistory);
    return newHistory;
  };

  const fetchHistory = async () => {
    history.value = await inventoryApi.getHistory();
  };

  return {
    categories,
    products,
    inventory,
    history,
    fetchCategories,
    createCategory,
    fetchProducts,
    createProduct,
    updateProduct,
    deleteProduct,
    fetchInventory,
    addTransaction,
    fetchHistory,
  };
});
