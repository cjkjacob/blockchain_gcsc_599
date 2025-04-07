// src/utils/auth.js

import API from '../services/api'

export async function refreshTokenIfNeeded() {
  const access = localStorage.getItem('jwt_access')
  const refresh = localStorage.getItem('jwt_refresh')

  if (!access || !refresh) return false

  const payload = JSON.parse(atob(access.split('.')[1]))
  const now = Math.floor(Date.now() / 1000)

  // If expired or about to expire in 60 seconds
  if (payload.exp < now + 60) {
    try {
      const res = await API.post('/token/refresh/', { refresh })
      const newAccess = res.data.access

      localStorage.setItem('jwt_access', newAccess)
      API.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`

      return true
    } catch (err) {
      console.error('Token refresh failed:', err)
      return false
    }
  }

  // Still valid
  return true
}


export function logoutUser(router) {
  // Remove tokens and wallet
  localStorage.removeItem('jwt_access')
  localStorage.removeItem('jwt_refresh')
  localStorage.removeItem('wallet_public')

  // Clear auth header
  delete API.defaults.headers.common['Authorization']

  // Redirect to login
  if (router) {
    router.push('/login').then(() => {
        window.location.reload()  // ✅ Force refresh to reflect UI changes
    })
  }
}
