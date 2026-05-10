<template>
  <div class="container">
    <div class="header-row">
      <RouterLink to="/inventory" class="back-link">← 在庫一覧に戻る</RouterLink>
      <h1 class="page-title">ロット詳細</h1>
    </div>

    <div v-if="loading" class="text-center">読み込み中...</div>
    <div v-else-if="!lot" class="alert alert-error">ロットが見つかりません。</div>
    <div v-else class="card">
      <div class="detail-grid">
        <div>
          <p class="detail-label">商品名</p>
          <p>{{ lot.product?.name ?? '-' }}</p>
        </div>
        <div>
          <p class="detail-label">カテゴリ</p>
          <p>{{ lot.product?.category?.name ?? '-' }}</p>
        </div>
        <div>
          <p class="detail-label">現在在庫</p>
          <p>{{ lot.quantity }}{{ lot.product?.unit ?? '' }}</p>
        </div>
        <div>
          <p class="detail-label">保管場所</p>
          <p>{{ lot.storage_location?.name ?? '-' }}</p>
        </div>
        <div>
          <p class="detail-label">賞味期限</p>
          <p>{{ formatDate(lot.expiry_date) }}</p>
        </div>
        <div>
          <p class="detail-label">購入日</p>
          <p>{{ formatDate(lot.purchased_date) }}</p>
        </div>
      </div>

      <form @submit.prevent="handleUse" class="usage-form">
        <div class="form-group">
          <label for="useQuantity">使用数量</label>
          <div class="quantity-row">
            <input
              id="useQuantity"
              v-model.number="useQuantity"
              type="number"
              min="0.1"
              step="0.1"
              class="input-field"
              required
            />
            <span class="unit-label">{{ lot.product?.unit ?? '' }}</span>
          </div>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="loading">使用登録</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInventoryStore } from '@/stores/inventory'
import { format } from 'date-fns'

const route = useRoute()
const router = useRouter()
const inventoryStore = useInventoryStore()
const useQuantity = ref(1)

const lot = computed(() => inventoryStore.currentLot)
const loading = computed(() => inventoryStore.loading)

onMounted(async () => {
  if (route.params.id) {
    await inventoryStore.fetchLotDetail(route.params.id as string)
  }
})

function formatDate(date: string | null) {
  if (!date) return '管理していません'
  return format(new Date(date), 'yyyy/MM/dd')
}

async function handleUse() {
  if (!lot.value) return
  if (useQuantity.value <= 0 || useQuantity.value > lot.value.quantity) {
    alert('使用数量が不正です')
    return
  }

  try {
    await inventoryStore.useProduct(lot.value.product_id, useQuantity.value)
    router.push({ name: 'inventory-list' })
  } catch (error) {
    alert('在庫の更新に失敗しました')
  }
}
</script>

<style scoped>
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.back-link {
  color: #2196f3;
  text-decoration: none;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.detail-label {
  margin: 0 0 8px;
  color: #616161;
}

.usage-form {
  max-width: 520px;
}

.quantity-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.unit-label {
  color: #555;
}

@media (max-width: 767px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
