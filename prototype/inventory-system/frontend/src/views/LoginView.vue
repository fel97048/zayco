<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const isLogin = ref(true);
const username = ref('');
const password = ref('');
const error = ref('');

const handleSubmit = async () => {
  error.value = '';
  try {
    if (isLogin.value) {
      await authStore.login({ username: username.value, password: password.value });
    } else {
      await authStore.register({ username: username.value, password: password.value });
    }
    router.push('/');
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'エラーが発生しました';
  }
};

const toggleMode = () => {
  isLogin.value = !isLogin.value;
  error.value = '';
};
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <h1>在庫管理システム</h1>
      <h2>{{ isLogin ? 'ログイン' : '新規登録' }}</h2>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>ユーザー名</label>
          <input v-model="username" type="text" required />
        </div>
        
        <div class="form-group">
          <label>パスワード</label>
          <input v-model="password" type="password" required />
        </div>
        
        <div v-if="error" class="error">{{ error }}</div>
        
        <button type="submit" class="primary btn-full">
          {{ isLogin ? 'ログイン' : '登録' }}
        </button>
      </form>
      
      <div class="toggle">
        <button @click="toggleMode" class="secondary">
          {{ isLogin ? '新規登録はこちら' : 'ログインはこちら' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  color: #667eea;
  margin-bottom: 10px;
  font-size: 24px;
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #555;
  font-size: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
}

.error {
  color: #f44336;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
  text-align: center;
}

.btn-full {
  width: 100%;
  padding: 12px;
  font-size: 16px;
}

.toggle {
  margin-top: 20px;
  text-align: center;
}

.toggle button {
  background: none;
  color: #667eea;
  padding: 5px 10px;
  text-decoration: underline;
}

.toggle button:hover {
  background: none;
  color: #764ba2;
}
</style>
