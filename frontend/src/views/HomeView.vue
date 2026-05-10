<template>
  <div class="container">
    <div class="page-title">ホーム</div>
    <div class="card stats-grid">
      <div class="stat-card">
        <p class="stat-title">商品数</p>
        <p class="stat-value">{{ summary?.product_count ?? '-' }}</p>
      </div>
      <div class="stat-card">
        <p class="stat-title">総在庫</p>
        <p class="stat-value">{{ summary?.total_quantity ?? '-' }}</p>
      </div>
      <div class="stat-card">
        <p class="stat-title">期限間近</p>
        <p class="stat-value">{{ summary?.expiring_count ?? '-' }}</p>
      </div>
      <div class="stat-card">
        <p class="stat-title">在庫少</p>
        <p class="stat-value">{{ summary?.low_stock_count ?? '-' }}</p>
      </div>
    </div>

    <div class="card section-card">
      <h2>期限が近い商品</h2>
      <table class="table">
        <thead>
          <tr>
            <th>商品名</th>
            <th>数量</th>
            <th>賞味期限</th>
            <th>残日数</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in summary?.expiring_items || []" :key="item.id">
            <td>{{ item.product.name }}</td>
            <td>{{ item.quantity }}{{ item.product.unit }}</td>
            <td>{{ formatDate(item.expiry_date) }}</td>
            <td>{{ item.remaining_days ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card section-card">
      <h2>在庫が少ない商品</h2>
      <table class="table">
        <thead>
          <tr>
            <th>商品名</th>
            <th>数量</th>
            <th>単位</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in summary?.low_stock_items || []" :key="item.id">
            <td>{{ item.product.name }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.product.unit }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useInventoryStore } from '@/stores/inventory'
import { format } from 'date-fns'

const inventoryStore = useInventoryStore()
const summary = computed(() => inventoryStore.summary)

onMounted(() => {
  inventoryStore.fetchSummary()
})

function formatDate(date: string | null) {
  if (!date) return '-'
  return format(new Date(date), 'yyyy/MM/dd')
}
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 16px;
  text-align: center;
}

.stat-title {
  font-size: 0.95rem;
  color: #616161;
  margin-bottom: 12px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
}

.section-card {
  margin-top: 20px;
}

@media (max-width: 1023px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 767px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
