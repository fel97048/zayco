import api from './index'

export default {
  async getAll(params = {}) {
    const response = await api.get('/products', { params })
    return response.data
  },

  async getById(id: string | number) {
    const response = await api.get(`/products/${id}`)
    return response.data
  },

  async create(data: any) {
    const response = await api.post('/products', data)
    return response.data
  },

  async update(id: string | number, data: any) {
    const response = await api.put(`/products/${id}`, data)
    return response.data
  },

  async delete(id: string | number) {
    const response = await api.delete(`/products/${id}`)
    return response.data
  },

  async search(keyword: string) {
    const response = await api.get('/products', { params: { search: keyword } })
    return response.data
  },

  async getCategories() {
    const response = await api.get('/categories')
    return response.data
  },

  async getStorageLocations() {
    const response = await api.get('/storage-locations')
    return response.data
  }
}
