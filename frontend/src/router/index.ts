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
