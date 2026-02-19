import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (username: string, password: string) => {
    try {
      const { data } = await axios.post('/api/v1/auth/login', { username, password })
      token.value = data.access_token
      localStorage.setItem('token', token.value)
      // 设置axios默认header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      return true
    } catch (error) {
      throw error
    }
  }

  const register = async (username: string, email: string, password: string) => {
    try {
      await axios.post('/api/v1/auth/register', { username, email, password })
      return true
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  const checkAuth = async () => {
    if (token.value) {
      try {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
        const { data } = await axios.get('/api/v1/auth/me')
        user.value = data
        return true
      } catch {
        logout()
        return false
      }
    }
    return false
  }

  // 初始化时检查认证状态
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth
  }
})