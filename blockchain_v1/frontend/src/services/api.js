// src/services/api.js
import axios from 'axios'

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// ✅ Add token if available
const token = localStorage.getItem('jwt_access')
if (token) {
  API.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

export default API
