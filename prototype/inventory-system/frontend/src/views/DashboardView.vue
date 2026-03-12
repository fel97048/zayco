<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useInventoryStore } from '@/stores/inventory';
import Layout from '@/components/Layout.vue';

const authStore = useAuthStore();
const inventoryStore = useInventoryStore();

onMounted(async () => {
  if (!authStore.user) {
    await authStore.fetchUser();
  }
  await Promise.all([
    inventoryStore.fetchCategories(),
    inventoryStore.fetchProducts(),
    inventoryStore.fetchInventory(),
  ]);
});

const lowStockItems = computed(() => {
  return inventoryStore.inventory.filter(item => item.quantity <= 5);
});

const totalProducts = computed(() => inventoryStore.products.length);
const totalCategories = computed(() => inventoryStore.categories.length);
const totalItems = computed(() => {
  return inventoryStore.inventory.reduce((sum, item) => sum + item.quantity, 0);
});
</script>

<template>
  <Layout>
    <div class="dashboard">
      <h1>ダッシュボード</h1>
      
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">{{ totalCategories }}</div>
          <div class="stat-label">カテゴリ数</div>
        </div>
        
        <div class="stat-card">
          <div class="stat-value">{{ totalProducts }}</div>
          <div class="stat-label">商品数</div>
        </div>
        
        <div class="stat-card">
          <div class="stat-value">{{ totalItems }}</div>
          <div class="stat-label">総在庫数</div>
        </div>
        
        <div class="stat-card warning">
          <div class="stat-value">{{ lowStockItems.length }}</div>
          <div class="stat-label">在庫少（5個以下）</div>
        </div>
      </div>
      
      <div v-if="lowStockItems.length > 0" class="low-stock-section">
        <h2>在庫が少ない商品</h2>
        <table>
          <thead>
            <tr>
              <th>商品名</th>
              <th>カテゴリ</th>
              <th>在庫数</th>
              <th>単位</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in lowStockItems" :key="item.id">
              <td>{{ item.product.name }}</td>
              <td>{{ item.product.category.name }}</td>
              <td class="quantity-warning">{{ item.quantity }}</td>
              <td>{{ item.product.unit }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Layout>
</template>

<style scoped>
.dashboard {
  max-width: 1200px;
}

h1 {
  margin-bottom: 30px;
  color: #333;
}

h2 {
  margin-bottom: 20px;
  color: #555;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card.warning {
  background: linear-gradient(135deg, #ff9a56 0%, #ff6a88 100%);
  color: white;
}

.stat-value {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 10px;
}

.stat-card.warning .stat-value {
  color: white;
}

.stat-label {
  font-size: 14px;
  color: #777;
}

.stat-card.warning .stat-label {
  color: white;
}

.low-stock-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quantity-warning {
  color: #f44336;
  font-weight: bold;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
