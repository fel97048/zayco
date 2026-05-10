<template>
  <div class="container">
    <div class="header-row">
      <div>
        <h1 class="page-title">在庫</h1>
      </div>
      <RouterLink to="/inventory/purchase" class="btn btn-primary">+ 購入登録</RouterLink>
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

      <div v-if="loading" class="text-center">読み込み中...</div>

      <div v-else>
        <table class="table inventory-table">
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
              class="clickable-row"
              :class="getRowClass(lot)"
              @click="goToDetail(lot.id)"
            >
              <td>{{ lot.product?.name ?? '-' }}</td>
              <td>{{ lot.quantity }}{{ lot.product?.unit ?? '' }}</td>
              <td>{{ lot.storage_location?.name ?? '-' }}</td>
              <td>{{ formatDate(lot.expiry_date) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
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

function goToDetail(id: string | number) {
  router.push({ name: 'lot-detail', params: { id } })
}

function formatDate(date: string | null) {
  if (!date) return '-'
  return format(new Date(date), 'yyyy/MM/dd')
}

function getRowClass(lot: any) {
  if (!lot.expiry_date) return ''

  const today = new Date()
  const expiry = new Date(lot.expiry_date)
  const daysUntilExpiry = Math.ceil((expiry.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))

  if (daysUntilExpiry <= 7) return 'expiring-soon'
  if (daysUntilExpiry <= 30) return 'expiring-warning'
  return ''
}
</script>

<style scoped>
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filters-row {
  margin-bottom: 20px;
}

.inventory-table th,
.inventory-table td {
  padding: 14px 12px;
}

.clickable-row {
  cursor: pointer;
}

.clickable-row:hover {
  background: #f5f5f5;
}

.expiring-soon {
  background-color: #ffebee;
}

.expiring-warning {
  background-color: #fff9c4;
}
</style>
