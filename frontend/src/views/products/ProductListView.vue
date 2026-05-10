<template>
  <div class="container">
    <div class="header-row">
      <h1 class="page-title">商品マスタ</h1>
      <RouterLink to="/products/new" class="btn btn-primary">+ 新規登録</RouterLink>
    </div>

    <div class="card">
      <div class="filters-row">
        <input
          v-model="searchQuery"
          type="text"
          class="input-field"
          placeholder="🔍 商品名で検索..."
          @input="handleSearch"
        />
      </div>

      <table class="table">
        <thead>
          <tr>
            <th>商品名</th>
            <th>カテゴリ</th>
            <th>単位</th>
            <th>保管場所</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id" class="clickable-row" @click="editProduct(product.id)">
            <td>{{ product.name }}</td>
            <td>{{ product.category?.name ?? '-' }}</td>
            <td>{{ product.unit }}</td>
            <td>{{ product.default_storage_location?.name ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import productsService from '@/api/products'

const router = useRouter()
const products = ref<any[]>([])
const searchQuery = ref('')

async function fetchProducts() {
  try {
    const data = await productsService.getAll({ search: searchQuery.value })
    products.value = Array.isArray(data) ? data : data.items || []
  } catch (error) {
    products.value = []
  }
}

onMounted(() => {
  fetchProducts()
})

function handleSearch() {
  fetchProducts()
}

function editProduct(id: number | string) {
  router.push({ name: 'product-edit', params: { id } })
}
</script>

<style scoped>
.filters-row {
  margin-bottom: 20px;
}

.clickable-row {
  cursor: pointer;
}

.clickable-row:hover {
  background: #f5f5f5;
}
</style>
