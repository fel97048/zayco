<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useInventoryStore } from '@/stores/inventory';
import Layout from '@/components/Layout.vue';

const inventoryStore = useInventoryStore();

const showModal = ref(false);
const selectedProductId = ref(0);
const transactionType = ref<'購入' | '使用'>('購入');
const quantity = ref(1);
const searchQuery = ref('');

onMounted(async () => {
  await Promise.all([
    inventoryStore.fetchProducts(),
    inventoryStore.fetchInventory(),
  ]);
});

const filteredInventory = computed(() => {
  if (!searchQuery.value) return inventoryStore.inventory;
  
  const query = searchQuery.value.toLowerCase();
  return inventoryStore.inventory.filter(item =>
    item.product.name.toLowerCase().includes(query) ||
    item.product.category.name.toLowerCase().includes(query)
  );
});

const openModal = (productId: number, type: '購入' | '使用') => {
  selectedProductId.value = productId;
  transactionType.value = type;
  quantity.value = 1;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const handleTransaction = async () => {
  try {
    await inventoryStore.addTransaction({
      product_id: selectedProductId.value,
      transaction_type: transactionType.value,
      quantity: quantity.value,
    });
    closeModal();
  } catch (error: any) {
    alert(error.response?.data?.detail || 'エラーが発生しました');
  }
};

const getStockClass = (quantity: number) => {
  if (quantity === 0) return 'stock-zero';
  if (quantity <= 5) return 'stock-low';
  return 'stock-ok';
};
</script>

<template>
  <Layout>
    <div class="inventory">
      <div class="header">
        <h1>在庫管理</h1>
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="商品名やカテゴリで検索..."
          />
        </div>
      </div>
      
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>商品名</th>
              <th>カテゴリ</th>
              <th>在庫数</th>
              <th>単位</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filteredInventory" :key="item.id">
              <td>{{ item.product.name }}</td>
              <td>{{ item.product.category.name }}</td>
              <td :class="getStockClass(item.quantity)">
                {{ item.quantity }}
              </td>
              <td>{{ item.product.unit }}</td>
              <td class="actions">
                <button
                  @click="openModal(item.product_id, '購入')"
                  class="primary btn-small"
                >
                  購入
                </button>
                <button
                  @click="openModal(item.product_id, '使用')"
                  class="secondary btn-small"
                  :disabled="item.quantity === 0"
                >
                  使用
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 在庫操作モーダル -->
      <div v-if="showModal" class="modal" @click.self="closeModal">
        <div class="modal-content">
          <h2>{{ transactionType }}</h2>
          <form @submit.prevent="handleTransaction">
            <div class="form-group">
              <label>数量</label>
              <input v-model.number="quantity" type="number" min="0.1" step="0.1" required />
            </div>
            
            <div class="modal-actions">
              <button type="button" @click="closeModal" class="secondary">
                キャンセル
              </button>
              <button type="submit" class="primary">
                {{ transactionType }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </Layout>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  gap: 20px;
}

.search-box {
  flex: 1;
  max-width: 400px;
}

.search-box input {
  width: 100%;
}

.table-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.actions {
  display: flex;
  gap: 10px;
}

.btn-small {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-small:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.stock-zero {
  color: #f44336;
  font-weight: bold;
}

.stock-low {
  color: #ff9800;
  font-weight: bold;
}

.stock-ok {
  color: #4CAF50;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
}

.modal-content h2 {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    max-width: 100%;
  }
  
  table {
    font-size: 12px;
  }
  
  .actions {
    flex-direction: column;
  }
}
</style>
