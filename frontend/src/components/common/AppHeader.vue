<template>
  <header class="app-header">
    <div class="brand" @click="goHome">在庫管理</div>
    <nav class="nav-links">
      <RouterLink to="/" class="nav-link" :class="{ active: isActive('/') }">ホーム</RouterLink>
      <RouterLink to="/inventory" class="nav-link" :class="{ active: isActive('/inventory') }">在庫</RouterLink>
      <RouterLink to="/shopping-list" class="nav-link" :class="{ active: isActive('/shopping-list') }">買い物リスト</RouterLink>
      <RouterLink to="/products" class="nav-link" :class="{ active: isActive('/products') }">商品マスタ</RouterLink>
      <RouterLink to="/settings" class="nav-link" :class="{ active: isActive('/settings') }">設定</RouterLink>
    </nav>
    <div class="user-actions">
      <span class="username">{{ authStore.user?.username || 'ユーザー' }}</span>
      <button class="btn btn-secondary" @click="logout">ログアウト</button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

function goHome() {
  router.push({ name: 'home' })
}

function logout() {
  authStore.logout()
  router.push({ name: 'login' })
}

function isActive(path: string) {
  return route.path === path
}
</script>

<style scoped>
.app-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 24px;
  background: #ffffff;
  border-bottom: 1px solid #e0e0e0;
}

.brand {
  font-size: 1.25rem;
  font-weight: 700;
  cursor: pointer;
}

.nav-links {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.nav-link {
  color: #333333;
  text-decoration: none;
  padding: 10px 14px;
  border-radius: 8px;
}

.nav-link.active {
  background: #4caf50;
  color: #ffffff;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  font-weight: 600;
}

@media (max-width: 767px) {
  .app-header {
    flex-direction: column;
    align-items: stretch;
  }

  .nav-links {
    justify-content: center;
  }
}
</style>
