<template>
  <div class="container">
    <div class="header-row">
      <RouterLink to="/products" class="back-link">← 商品一覧に戻る</RouterLink>
      <h1 class="page-title">商品編集</h1>
    </div>

    <div v-if="loading" class="text-center">読み込み中...</div>
    <div v-else-if="!product" class="alert alert-error">商品が見つかりません。</div>
    <div v-else class="card product-form-card">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="name">商品名 *</label>
          <input id="name" v-model="form.name" type="text" class="input-field" required />
        </div>

        <div class="form-group">
          <label for="category">カテゴリ *</label>
          <select id="category" v-model="form.category_id" class="select-field" required>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="storage">デフォルト保管場所 *</label>
          <select id="storage" v-model="form.default_storage_location_id" class="select-field" required>
            <option v-for="location in storageLocations" :key="location.id" :value="location.id">
              {{ location.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="unit">単位 *</label>
          <select id="unit" v-model="form.unit" class="select-field" required>
            <option value="個">個</option>
            <option value="本">本</option>
            <option value="袋">袋</option>
            <option value="ml">ml</option>
            <option value="g">g</option>
            <option value="kg">kg</option>
            <option value="L">L</option>
          </select>
        </div>

        <div class="form-group">
          <label for="barcode">バーコード（任意）</label>
          <input id="barcode" v-model="form.barcode" type="text" class="input-field" />
        </div>

        <div class="form-group">
          <label for="note">備考（任意）</label>
          <textarea id="note" v-model="form.note" class="textarea-field"></textarea>
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-danger" @click="handleDelete">削除</button>
          <RouterLink to="/products" class="btn btn-secondary">キャンセル</RouterLink>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? '更新中...' : '更新' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import productsService from '@/api/products'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const categories = ref<any[]>([])
const storageLocations = ref<any[]>([])
const product = ref<any>(null)

const form = ref({
  name: '',
  category_id: null,
  default_storage_location_id: null,
  unit: '個',
  barcode: '',
  note: ''
})

async function fetchMeta() {
  categories.value = await productsService.getCategories()
  storageLocations.value = await productsService.getStorageLocations()
}

async function fetchProduct() {
  if (!route.params.id) return
  const id = route.params.id as string
  product.value = await productsService.getById(id)
  if (product.value) {
    form.value = {
      name: product.value.name,
      category_id: product.value.category_id,
      default_storage_location_id: product.value.default_storage_location_id,
      unit: product.value.unit,
      barcode: product.value.barcode || '',
      note: product.value.note || ''
    }
  }
}

onMounted(async () => {
  await fetchMeta()
  await fetchProduct()
})

async function handleSubmit() {
  if (!route.params.id) return
  loading.value = true
  try {
    await productsService.update(route.params.id as string, form.value)
    router.push({ name: 'products' })
  } catch (error) {
    alert('商品更新に失敗しました')
  } finally {
    loading.value = false
  }
}

async function handleDelete() {
  if (!route.params.id) return
  if (!confirm('本当に削除しますか？')) return
  loading.value = true
  try {
    await productsService.delete(route.params.id as string)
    router.push({ name: 'products' })
  } catch (error) {
    alert('商品削除に失敗しました')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.product-form-card {
  max-width: 700px;
  margin: 0 auto;
}

.back-link {
  color: #2196f3;
  text-decoration: none;
}
</style>
