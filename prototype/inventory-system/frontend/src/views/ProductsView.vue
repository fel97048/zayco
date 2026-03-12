<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useInventoryStore } from '@/stores/inventory';
import Layout from '@/components/Layout.vue';

const inventoryStore = useInventoryStore();

const showModal = ref(false);
const showCategoryModal = ref(false);
const editingProduct = ref<any>(null);
const newCategoryName = ref('');

const formData = ref({
  name: '',
  category_id: 0,
  barcode: '',
  unit: '個',
});

const units = ['個', '本', '袋', 'ml', 'g', 'kg', 'L'];

onMounted(async () => {
  await Promise.all([
    inventoryStore.fetchCategories(),
    inventoryStore.fetchProducts(),
  ]);
});

const openModal = (product?: any) => {
  if (product) {
    editingProduct.value = product;
    formData.value = {
      name: product.name,
      category_id: product.category_id,
      barcode: product.barcode || '',
      unit: product.unit,
    };
  } else {
    editingProduct.value = null;
    formData.value = {
      name: '',
      category_id: inventoryStore.categories[0]?.id || 0,
      barcode: '',
      unit: '個',
    };
  }
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingProduct.value = null;
};

const handleSubmit = async () => {
  try {
    if (editingProduct.value) {
      await inventoryStore.updateProduct(editingProduct.value.id, formData.value);
    } else {
      await inventoryStore.createProduct(formData.value);
    }
    closeModal();
  } catch (error: any) {
    alert(error.response?.data?.detail || 'エラーが発生しました');
  }
};

const handleDelete = async (id: number) => {
  if (confirm('この商品を削除してもよろしいですか？')) {
    try {
      await inventoryStore.deleteProduct(id);
    } catch (error: any) {
      alert(error.response?.data?.detail || 'エラーが発生しました');
    }
  }
};

const handleCreateCategory = async () => {
  if (!newCategoryName.value.trim()) return;
  
  try {
    await inventoryStore.createCategory(newCategoryName.value);
    newCategoryName.value = '';
    showCategoryModal.value = false;
  } catch (error: any) {
    alert(error.response?.data?.detail || 'エラーが発生しました');
  }
};
</script>

<template>
  <Layout>
    <div class="products">
      <div class="header">
        <h1>商品管理</h1>
        <div class="header-actions">
          <button @click="showCategoryModal = true" class="secondary">
            カテゴリ追加
          </button>
          <button @click="openModal()" class="primary">
            商品追加
          </button>
        </div>
      </div>
      
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>商品名</th>
              <th>カテゴリ</th>
              <th>バーコード</th>
              <th>単位</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in inventoryStore.products" :key="product.id">
              <td>{{ product.name }}</td>
              <td>{{ product.category.name }}</td>
              <td>{{ product.barcode || '-' }}</td>
              <td>{{ product.unit }}</td>
              <td class="actions">
                <button @click="openModal(product)" class="secondary btn-small">
                  編集
                </button>
                <button @click="handleDelete(product.id)" class="danger btn-small">
                  削除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 商品追加/編集モーダル -->
      <div v-if="showModal" class="modal" @click.self="closeModal">
        <div class="modal-content">
          <h2>{{ editingProduct ? '商品編集' : '商品追加' }}</h2>
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label>商品名</label>
              <input v-model="formData.name" type="text" required />
            </div>
            
            <div class="form-group">
              <label>カテゴリ</label>
              <select v-model.number="formData.category_id" required>
                <option v-for="cat in inventoryStore.categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label>バーコード（任意）</label>
              <input v-model="formData.barcode" type="text" />
            </div>
            
            <div class="form-group">
              <label>単位</label>
              <select v-model="formData.unit" required>
                <option v-for="unit in units" :key="unit" :value="unit">
                  {{ unit }}
                </option>
              </select>
            </div>
            
            <div class="modal-actions">
              <button type="button" @click="closeModal" class="secondary">
                キャンセル
              </button>
              <button type="submit" class="primary">
                {{ editingProduct ? '更新' : '追加' }}
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <!-- カテゴリ追加モーダル -->
      <div v-if="showCategoryModal" class="modal" @click.self="showCategoryModal = false">
        <div class="modal-content">
          <h2>カテゴリ追加</h2>
          <form @submit.prevent="handleCreateCategory">
            <div class="form-group">
              <label>カテゴリ名</label>
              <input v-model="newCategoryName" type="text" required />
            </div>
            
            <div class="modal-actions">
              <button type="button" @click="showCategoryModal = false" class="secondary">
                キャンセル
              </button>
              <button type="submit" class="primary">
                追加
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
}

.header-actions {
  display: flex;
  gap: 10px;
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
  max-width: 500px;
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
    align-items: flex-start;
    gap: 15px;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .header-actions button {
    flex: 1;
  }
  
  table {
    font-size: 12px;
  }
  
  .actions {
    flex-direction: column;
  }
}
</style>
