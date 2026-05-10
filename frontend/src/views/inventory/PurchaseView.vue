<template>
  <div class="container">
    <div class="header-row">
      <RouterLink to="/inventory" class="back-link">← 在庫一覧に戻る</RouterLink>
      <h1 class="page-title">購入登録</h1>
    </div>

    <div class="card purchase-card">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="product">商品名 *</label>
          <input
            id="product"
            v-model="searchQuery"
            type="text"
            class="input-field"
            placeholder="商品名を入力..."
            @input="searchProducts"
            required
          />
          <div v-if="suggestions.length" class="suggestions">
            <button
              v-for="product in suggestions"
              :key="product.id"
              type="button"
              class="suggestion-item"
              @click="selectProduct(product)"
            >
              {{ product.name }}
            </button>
          </div>
        </div>

        <div v-if="selectedProduct" class="form-group">
          <label for="quantity">数量 *</label>
          <div class="quantity-row">
            <input
              id="quantity"
              v-model.number="form.quantity"
              type="number"
              step="0.1"
              min="0.1"
              class="input-field"
              required
            />
            <span class="unit-label">{{ selectedProduct.unit }}</span>
          </div>
        </div>

        <div v-if="selectedProduct" class="form-group">
          <label for="storage">保管場所</label>
          <select id="storage" v-model="form.storage_location_id" class="select-field">
            <option v-for="location in storageLocations" :key="location.id" :value="location.id">
              {{ location.name }}
            </option>
          </select>
          <p class="hint">※ デフォルト値が設定されています</p>
        </div>

        <div v-if="selectedProduct" class="form-group">
          <label for="expiry">賞味期限（任意）</label>
          <input id="expiry" v-model="form.expiry_date" type="date" class="input-field" />
        </div>

        <div class="form-actions">
          <RouterLink to="/inventory" class="btn btn-secondary">キャンセル</RouterLink>
          <button type="submit" class="btn btn-primary" :disabled="!selectedProduct || loading">
            {{ loading ? '登録中...' : '登録' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useInventoryStore } from '@/stores/inventory'
import productsService from '@/api/products'

const router = useRouter()
const inventoryStore = useInventoryStore()

const searchQuery = ref('')
const suggestions = ref<any[]>([])
const selectedProduct = ref<any>(null)
const storageLocations = ref<any[]>([])
const loading = ref(false)

const form = reactive({
  product_id: null,
  quantity: 1,
  storage_location_id: null,
  expiry_date: '',
  purchased_date: new Date().toISOString().split('T')[0]
})

async function searchProducts() {
  if (searchQuery.value.length < 2) {
    suggestions.value = []
    return
  }

  try {
    const data = await productsService.search(searchQuery.value)
    suggestions.value = Array.isArray(data) ? data : data.items || []
  } catch (error) {
    suggestions.value = []
  }
}

function selectProduct(product: any) {
  selectedProduct.value = product
  searchQuery.value = product.name
  suggestions.value = []

  form.product_id = product.id
  form.storage_location_id = product.default_storage_location_id ?? null
  loadStorageLocations()
}

async function loadStorageLocations() {
  try {
    const data = await productsService.getStorageLocations()
    storageLocations.value = Array.isArray(data) ? data : data.items || []

    if (!form.storage_location_id && storageLocations.value.length) {
      form.storage_location_id = storageLocations.value[0].id
    }
  } catch (error) {
    storageLocations.value = []
  }
}

async function handleSubmit() {
  if (!selectedProduct.value) return
  loading.value = true

  try {
    await inventoryStore.purchaseProduct({
      product_id: form.product_id,
      transaction_type: '購入',
      quantity: form.quantity,
      storage_location_id: form.storage_location_id,
      expiry_date: form.expiry_date || null,
      purchased_date: form.purchased_date
    })
    router.push({ name: 'inventory-list' })
  } catch (error) {
    alert('登録に失敗しました')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.purchase-card {
  max-width: 700px;
  margin: 0 auto;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.back-link {
  color: #2196f3;
  text-decoration: none;
}

.quantity-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.unit-label {
  font-size: 1rem;
  color: #555;
}

.suggestions {
  display: grid;
  margin-top: 8px;
  border: 1px solid #dddddd;
  border-radius: 8px;
  background: #ffffff;
}

.suggestion-item {
  width: 100%;
  padding: 12px 14px;
  border: none;
  text-align: left;
  background: transparent;
  cursor: pointer;
}

.suggestion-item:hover {
  background: #f5f5f5;
}

.hint {
  margin-top: 8px;
  font-size: 0.9rem;
  color: #666;
}

.form-actions {
  margin-top: 24px;
}
</style>
