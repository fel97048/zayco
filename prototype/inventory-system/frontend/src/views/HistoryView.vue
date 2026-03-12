<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useInventoryStore } from '@/stores/inventory';
import Layout from '@/components/Layout.vue';

const inventoryStore = useInventoryStore();

onMounted(async () => {
  await Promise.all([
    inventoryStore.fetchProducts(),
    inventoryStore.fetchHistory(),
  ]);
});

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const getProductName = (productId: number) => {
  const product = inventoryStore.products.find(p => p.id === productId);
  return product?.name || '不明';
};

const getTransactionClass = (type: string) => {
  return type === '購入' ? 'transaction-purchase' : 'transaction-use';
};
</script>

<template>
  <Layout>
    <div class="history">
      <h1>在庫履歴</h1>
      
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>日時</th>
              <th>商品名</th>
              <th>種別</th>
              <th>数量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in inventoryStore.history" :key="record.id">
              <td>{{ formatDate(record.created_at) }}</td>
              <td>{{ getProductName(record.product_id) }}</td>
              <td :class="getTransactionClass(record.transaction_type)">
                {{ record.transaction_type }}
              </td>
              <td>{{ record.quantity }}</td>
            </tr>
          </tbody>
        </table>
        
        <div v-if="inventoryStore.history.length === 0" class="no-data">
          履歴がありません
        </div>
      </div>
    </div>
  </Layout>
</template>

<style scoped>
h1 {
  margin-bottom: 30px;
}

.table-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.transaction-purchase {
  color: #4CAF50;
  font-weight: bold;
}

.transaction-use {
  color: #2196F3;
  font-weight: bold;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
}

@media (max-width: 768px) {
  table {
    font-size: 12px;
  }
}
</style>
