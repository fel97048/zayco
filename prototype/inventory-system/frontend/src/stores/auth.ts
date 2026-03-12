import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { User, LoginRequest, RegisterRequest } from '@/types';
import { authApi } from '@/api';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const token = ref<string | null>(localStorage.getItem('token'));
  const isAuthenticated = ref(!!token.value);

  const login = async (credentials: LoginRequest) => {
    const response = await authApi.login(credentials);
    token.value = response.access_token;
    localStorage.setItem('token', response.access_token);
    isAuthenticated.value = true;
    await fetchUser();
  };

  const register = async (credentials: RegisterRequest) => {
    await authApi.register(credentials);
    await login({ username: credentials.username, password: credentials.password });
  };

  const logout = () => {
    user.value = null;
    token.value = null;
    localStorage.removeItem('token');
    isAuthenticated.value = false;
  };

  const fetchUser = async () => {
    try {
      user.value = await authApi.getMe();
    } catch (error) {
      logout();
      throw error;
    }
  };

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser,
  };
});
