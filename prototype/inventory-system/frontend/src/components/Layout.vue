<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const logout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<template>
  <div class="layout">
    <nav class="navbar">
      <div class="nav-brand">在庫管理システム</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">ダッシュボード</router-link>
        <router-link to="/products" class="nav-link">商品管理</router-link>
        <router-link to="/inventory" class="nav-link">在庫管理</router-link>
        <router-link to="/history" class="nav-link">履歴</router-link>
      </div>
      <div class="nav-user">
        <span v-if="authStore.user">{{ authStore.user.username }}</span>
        <button @click="logout" class="danger">ログアウト</button>
      </div>
    </nav>
    
    <main class="main-content">
      <slot></slot>
    </main>
  </div>
</template>

<style scoped>
.layout {
  min-height: 100vh;
}

.navbar {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px 30px;
  display: flex;
  align-items: center;
  gap: 30px;
}

.nav-brand {
  font-size: 20px;
  font-weight: bold;
  color: #667eea;
}

.nav-links {
  display: flex;
  gap: 20px;
  flex: 1;
}

.nav-link {
  text-decoration: none;
  color: #555;
  padding: 8px 15px;
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: #667eea;
  color: white;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 15px;
}

.nav-user span {
  color: #555;
  font-weight: 500;
}

.main-content {
  padding: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 15px;
  }
  
  .nav-links {
    flex-direction: column;
    width: 100%;
  }
  
  .nav-user {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
