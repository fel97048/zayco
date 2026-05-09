# Vue.js 実装ガイド

## 改訂履歴

| 版 | 日付 | 変更内容 |
|---|------|---------|
| 1.0 | 2025-03-11 | 初版作成 |

## 1. 概要

在庫管理システムのフロントエンドをVue 3で実装するためのガイドです。

### 1.1 技術スタック

- **Vue 3**: Composition API使用
- **Vue Router 4**: SPA ルーティング
- **Pinia**: 状態管理
- **Axios**: HTTP通信
- **Vite**: ビルドツール
- **TypeScript**: オプション（推奨）

## 2. プロジェクト構造

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── assets/              # 静的ファイル
│   │   └── styles/
│   │       └── main.css
│   ├── components/          # 共通コンポーネント
│   │   ├── common/
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppButton.vue
│   │   │   ├── AppInput.vue
│   │   │   └── AppTable.vue
│   │   └── inventory/
│   │       ├── InventoryTable.vue
│   │       └── LotCard.vue
│   ├── views/               # ページコンポーネント
│   │   ├── LoginView.vue
│   │   ├── HomeView.vue
│   │   ├── inventory/
│   │   │   ├── InventoryListView.vue
│   │   │   ├── LotDetailView.vue
│   │   │   └── PurchaseView.vue
│   │   ├── shopping/
│   │   │   ├── ShoppingListView.vue
│   │   │   └── ManualAddView.vue
│   │   ├── products/
│   │   │   ├── ProductListView.vue
│   │   │   ├── ProductNewView.vue
│   │   │   └── ProductEditView.vue
│   │   └── SettingsView.vue
│   ├── stores/              # Pinia stores
│   │   ├── auth.js
│   │   ├── inventory.js
│   │   ├── products.js
│   │   └── shopping.js
│   ├── services/            # API通信
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── inventory.js
│   │   ├── products.js
│   │   └── shopping.js
│   ├── router/              # ルーティング
│   │   └── index.js
│   ├── utils/               # ユーティリティ
│   │   ├── formatters.js
│   │   └── validators.js
│   ├── App.vue              # ルートコンポーネント
│   └── main.js              # エントリーポイント
├── .env.development         # 環境変数（開発）
├── .env.production          # 環境変数（本番）
├── index.html
├── package.json
└── vite.config.js
```

## 3. 初期セットアップ

### 3.1 プロジェクト作成

```bash
# Viteで作成
npm create vite@latest inventory-frontend -- --template vue

cd inventory-frontend

# 依存パッケージインストール
npm install vue-router@4 pinia axios date-fns

# 開発サーバー起動
npm run dev
```

### 3.2 package.json

```json
{
  "name": "inventory-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0",
    "axios": "^1.6.0",
    "date-fns": "^3.0.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.0"
  }
}
```

### 3.3 環境変数

**.env.development:**
```
VITE_API_BASE_URL=http://localhost:8000
```

**.env.production:**
```
VITE_API_BASE_URL=https://api.inventory.example.com
```

## 4. ルーティング設定

### 4.1 router/index.js

```javascript
// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/inventory',
    name: 'inventory-list',
    component: () => import('@/views/inventory/InventoryListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/inventory/lots/:id',
    name: 'lot-detail',
    component: () => import('@/views/inventory/LotDetailView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/inventory/purchase',
    name: 'purchase',
    component: () => import('@/views/inventory/PurchaseView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/shopping-list',
    name: 'shopping-list',
    component: () => import('@/views/shopping/ShoppingListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/shopping-list/add',
    name: 'shopping-add',
    component: () => import('@/views/shopping/ManualAddView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('@/views/products/ProductListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/products/new',
    name: 'product-new',
    component: () => import('@/views/products/ProductNewView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/products/:id/edit',
    name: 'product-edit',
    component: () => import('@/views/products/ProductEditView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/SettingsView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ナビゲーションガード
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
```

## 5. API通信設定

### 5.1 services/api.js

```javascript
// src/services/api.js

import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL + '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// リクエストインターセプター（トークン付与）
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// レスポンスインターセプター（エラーハンドリング）
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      router.push({ name: 'login' })
    }
    return Promise.reject(error)
  }
)

export default api
```

### 5.2 services/auth.js

```javascript
// src/services/auth.js

import api from './api'

export default {
  async login(username, password) {
    const response = await api.post('/users/login/', {
      username,
      password
    })
    return response.data
  },

  async register(username, password) {
    const response = await api.post('/users/register/', {
      username,
      password
    })
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/users/me/')
    return response.data
  }
}
```

### 5.3 services/inventory.js

```javascript
// src/services/inventory.js

import api from './api'

export default {
  async getLots(params = {}) {
    const response = await api.get('/inventory/lots/', { params })
    return response.data
  },

  async getLotDetail(id) {
    const response = await api.get(`/inventory/lots/${id}/`)
    return response.data
  },

  async purchase(data) {
    const response = await api.post('/inventory/lots/purchase/', data)
    return response.data
  },

  async useLot(id, quantity) {
    const response = await api.post(`/inventory/lots/${id}/use/`, {
      quantity
    })
    return response.data
  },

  async getSummary() {
    const response = await api.get('/inventory/summary/')
    return response.data
  }
}
```

## 6. Pinia Store設計

### 6.1 stores/auth.js

```javascript
// src/stores/auth.js

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)

  // Actions
  async function login(username, password) {
    const data = await authService.login(username, password)
    token.value = data.access
    localStorage.setItem('token', data.access)
    await fetchUser()
  }

  async function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      user.value = await authService.getCurrentUser()
    } catch (error) {
      logout()
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    fetchUser
  }
})
```

### 6.2 stores/inventory.js

```javascript
// src/stores/inventory.js

import { defineStore } from 'pinia'
import { ref } from 'vue'
import inventoryService from '@/services/inventory'

export const useInventoryStore = defineStore('inventory', () => {
  // State
  const lots = ref([])
  const currentLot = ref(null)
  const summary = ref(null)
  const loading = ref(false)

  // Actions
  async function fetchLots(params = {}) {
    loading.value = true
    try {
      const data = await inventoryService.getLots(params)
      lots.value = data.items || data
    } finally {
      loading.value = false
    }
  }

  async function fetchLotDetail(id) {
    loading.value = true
    try {
      currentLot.value = await inventoryService.getLotDetail(id)
    } finally {
      loading.value = false
    }
  }

  async function purchaseProduct(data) {
    await inventoryService.purchase(data)
    await fetchLots() // 一覧を再取得
  }

  async function useProduct(id, quantity) {
    await inventoryService.useLot(id, quantity)
    await fetchLots() // 一覧を再取得
  }

  async function fetchSummary() {
    summary.value = await inventoryService.getSummary()
  }

  return {
    lots,
    currentLot,
    summary,
    loading,
    fetchLots,
    fetchLotDetail,
    purchaseProduct,
    useProduct,
    fetchSummary
  }
})
```

## 7. 主要コンポーネント実装例

### 7.1 App.vue

```vue
<!-- src/App.vue -->
<template>
  <div id="app">
    <AppHeader v-if="isAuthenticated" />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/common/AppHeader.vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

onMounted(() => {
  if (authStore.token) {
    authStore.fetchUser()
  }
})
</script>

<style>
#app {
  font-family: sans-serif;
  min-height: 100vh;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
```

### 7.2 LoginView.vue

```vue
<!-- src/views/LoginView.vue -->
<template>
  <div class="login-container">
    <div class="login-card">
      <h1>在庫管理システム</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">ユーザー名</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">パスワード</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
          />
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? 'ログイン中...' : 'ログイン' }}
        </button>

        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    await authStore.login(username.value, password.value)
    router.push({ name: 'home' })
  } catch (err) {
    error.value = 'ユーザー名またはパスワードが正しくありません'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error {
  color: #f44336;
  margin-top: 10px;
}
</style>
```

### 7.3 InventoryListView.vue

```vue
<!-- src/views/inventory/InventoryListView.vue -->
<template>
  <div class="inventory-list">
    <div class="header">
      <h1>在庫</h1>
      <router-link to="/inventory/purchase" class="btn-primary">
        + 購入登録
      </router-link>
    </div>

    <div class="filters">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="🔍 商品名で検索..."
        @input="handleSearch"
      />
    </div>

    <div v-if="loading" class="loading">読み込み中...</div>

    <table v-else class="inventory-table">
      <thead>
        <tr>
          <th>商品名</th>
          <th>数量</th>
          <th>保管場所</th>
          <th>賞味期限</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="lot in lots"
          :key="lot.id"
          @click="goToDetail(lot.id)"
          class="clickable"
          :class="getRowClass(lot)"
        >
          <td>{{ lot.product.name }}</td>
          <td>{{ lot.quantity }}{{ lot.product.unit }}</td>
          <td>{{ lot.storage_location.name }}</td>
          <td>{{ formatDate(lot.expiry_date) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useInventoryStore } from '@/stores/inventory'
import { format } from 'date-fns'

const router = useRouter()
const inventoryStore = useInventoryStore()

const searchQuery = ref('')
const loading = computed(() => inventoryStore.loading)
const lots = computed(() => inventoryStore.lots)

onMounted(() => {
  inventoryStore.fetchLots()
})

function handleSearch() {
  inventoryStore.fetchLots({ search: searchQuery.value })
}

function goToDetail(id) {
  router.push({ name: 'lot-detail', params: { id } })
}

function formatDate(date) {
  if (!date) return '-'
  return format(new Date(date), 'yyyy/MM/dd')
}

function getRowClass(lot) {
  if (!lot.expiry_date) return ''
  
  const today = new Date()
  const expiry = new Date(lot.expiry_date)
  const daysUntilExpiry = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24))
  
  if (daysUntilExpiry <= 7) return 'expiring-soon'
  if (daysUntilExpiry <= 30) return 'expiring-warning'
  return ''
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 4px;
}

.filters {
  margin-bottom: 20px;
}

input[type="text"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.inventory-table {
  width: 100%;
  border-collapse: collapse;
}

.inventory-table th,
.inventory-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.inventory-table th {
  background-color: #f8f9fa;
  font-weight: 500;
}

.inventory-table tr.clickable {
  cursor: pointer;
}

.inventory-table tr.clickable:hover {
  background-color: #f5f5f5;
}

.expiring-soon {
  background-color: #ffebee;
}

.expiring-warning {
  background-color: #fff9c4;
}
</style>
```

### 7.4 PurchaseView.vue

```vue
<!-- src/views/inventory/PurchaseView.vue -->
<template>
  <div class="purchase-view">
    <div class="header">
      <router-link to="/inventory" class="back-link">
        ← 在庫一覧に戻る
      </router-link>
      <h1>購入登録</h1>
    </div>

    <form @submit.prevent="handleSubmit" class="purchase-form">
      <div class="form-group">
        <label for="product">商品名 *</label>
        <input
          id="product"
          v-model="searchQuery"
          type="text"
          placeholder="商品名を入力..."
          @input="searchProducts"
          required
        />
        <div v-if="suggestions.length" class="suggestions">
          <div
            v-for="product in suggestions"
            :key="product.id"
            @click="selectProduct(product)"
            class="suggestion-item"
          >
            {{ product.name }}
          </div>
        </div>
      </div>

      <div v-if="selectedProduct" class="form-group">
        <label for="quantity">数量 *</label>
        <input
          id="quantity"
          v-model.number="form.quantity"
          type="number"
          step="0.1"
          min="0.1"
          required
        />
        <span class="unit">{{ selectedProduct.unit }}</span>
      </div>

      <div v-if="selectedProduct" class="form-group">
        <label for="storage">保管場所</label>
        <select id="storage" v-model="form.storage_location_id">
          <option
            v-for="location in storageLocations"
            :key="location.id"
            :value="location.id"
          >
            {{ location.name }}
          </option>
        </select>
        <p class="hint">※ デフォルト値が設定されています</p>
      </div>

      <div v-if="selectedProduct" class="form-group">
        <label for="expiry">賞味期限（任意）</label>
        <input
          id="expiry"
          v-model="form.expiry_date"
          type="date"
        />
      </div>

      <div class="form-actions">
        <router-link to="/inventory" class="btn-secondary">
          キャンセル
        </router-link>
        <button type="submit" class="btn-primary" :disabled="!selectedProduct">
          登録
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useInventoryStore } from '@/stores/inventory'
import productsService from '@/services/products'

const router = useRouter()
const inventoryStore = useInventoryStore()

const searchQuery = ref('')
const suggestions = ref([])
const selectedProduct = ref(null)
const storageLocations = ref([])

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

  const data = await productsService.search(searchQuery.value)
  suggestions.value = data.items || data
}

function selectProduct(product) {
  selectedProduct.value = product
  searchQuery.value = product.name
  suggestions.value = []
  
  form.product_id = product.id
  form.storage_location_id = product.default_storage_location.id
  
  loadStorageLocations()
}

async function loadStorageLocations() {
  const data = await productsService.getStorageLocations()
  storageLocations.value = data
}

async function handleSubmit() {
  try {
    await inventoryStore.purchaseProduct(form)
    router.push({ name: 'inventory-list' })
  } catch (error) {
    alert('登録に失敗しました')
  }
}
</script>

<style scoped>
.purchase-view {
  max-width: 600px;
  margin: 0 auto;
}

.header {
  margin-bottom: 30px;
}

.back-link {
  color: #2196F3;
  text-decoration: none;
  margin-bottom: 10px;
  display: inline-block;
}

.purchase-form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

input, select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.unit {
  margin-left: 10px;
  color: #777;
}

.suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-top: none;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.suggestion-item {
  padding: 10px;
  cursor: pointer;
}

.suggestion-item:hover {
  background-color: #f5f5f5;
}

.hint {
  font-size: 14px;
  color: #777;
  margin-top: 5px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.btn-primary, .btn-secondary {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 4px;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
}
</style>
```

## 8. main.js

```javascript
// src/main.js

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/styles/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
```

## 9. vite.config.js

```javascript
// vite.config.js

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

## 10. Docker対応

### 10.1 Dockerfile

```dockerfile
# frontend/Dockerfile

FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host"]
```

### 10.2 docker-compose.yml更新

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DEBUG=True

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
```

## 11. 開発ワークフロー

### 11.1 開発サーバー起動

```bash
# フロントエンドのみ
cd frontend
npm run dev

# Docker使用
docker-compose up
```

### 11.2 ビルド

```bash
npm run build
```

ビルド成果物: `dist/` ディレクトリ

### 11.3 本番デプロイ

```bash
# ビルド
npm run build

# dist/ ディレクトリを静的ホスティングサービスにデプロイ
# - Netlify
# - Vercel
# - Firebase Hosting
# など
```

## 12. 実装の優先順位

### Phase 1: 基本機能
1. ✅ プロジェクトセットアップ
2. ✅ ルーティング設定
3. ✅ 認証機能（Login）
4. ✅ 在庫一覧表示
5. ✅ 購入登録

### Phase 2: 拡張機能
6. ロット詳細・使用登録
7. 買い物リスト
8. 商品マスタ管理
9. 設定画面

### Phase 3: UX改善
10. ローディング状態
11. エラーハンドリング
12. レスポンシブ対応
13. アクセシビリティ

## 13. まとめ

Vue 3実装のポイント:

- **Composition API**: より柔軟で再利用可能なコード
- **Pinia**: シンプルで型安全な状態管理
- **Vue Router**: SPA ルーティング
- **Axios**: HTTP通信の簡潔な実装

次のステップ: 残りのビューコンポーネントと共通コンポーネントの実装
