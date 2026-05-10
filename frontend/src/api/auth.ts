import api from './index'

export default {
  async login(username: string, password: string) {
    const response = await api.post('/users/login', { username, password })
    return response.data
  },

  async register(username: string, password: string) {
    const response = await api.post('/users/register', { username, password })
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/users/me')
    return response.data
  }
}
