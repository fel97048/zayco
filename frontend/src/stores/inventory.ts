import { defineStore } from 'pinia'
import { ref } from 'vue'
import inventoryService from '@/services/inventory'

export const useInventoryStore = defineStore('inventory', () => {
  const lots = ref<any[]>([])
  const currentLot = ref<any>(null)
  const summary = ref<any>(null)
  const loading = ref(false)

  async function fetchLots(params = {}) {
    loading.value = true
    try {
      const data = await inventoryService.getLots(params)
      lots.value = Array.isArray(data) ? data : data.items || []
    } finally {
      loading.value = false
    }
  }

  async function fetchLotDetail(id: string | number) {
    loading.value = true
    try {
      currentLot.value = await inventoryService.getLotDetail(id)
    } finally {
      loading.value = false
    }
  }

  async function purchaseProduct(data: any) {
    await inventoryService.purchase(data)
    await fetchLots()
  }

  async function useProduct(id: string | number, quantity: number) {
    await inventoryService.useLot(id, quantity)
    await fetchLots()
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
