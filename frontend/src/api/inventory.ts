import api from './index'

export default {
  async getLots(params = {}) {
    const response = await api.get('/inventory', { params })
    return response.data
  },

  async getLotDetail(id: string | number) {
    const response = await api.get(`/inventory/${id}`)
    return response.data
  },

  async purchase(data: any) {
    const response = await api.post('/inventory/transaction', data)
    return response.data
  },

  async useLot(id: string | number, quantity: number) {
    const response = await api.post('/inventory/transaction', {
      product_id: id,
      transaction_type: '使用',
      quantity
    })
    return response.data
  },

  async getSummary() {
    const response = await api.get('/inventory/summary')
    return response.data
  }
}
