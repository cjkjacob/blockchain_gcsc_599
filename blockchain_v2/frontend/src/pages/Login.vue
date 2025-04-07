<template>
    <div class="max-w-md mx-auto p-6">
      <h1 class="text-2xl font-bold mb-4">🔐 Login</h1>
  
      <form @submit.prevent="login" class="space-y-4">
        <input v-model="form.username" type="text" placeholder="Username" class="input w-full border rounded px-3 py-2 bg-white text-white dark:bg-gray-800 dark:text-white;" required />
        <input v-model="form.password" type="password" placeholder="Password" class="input w-full border rounded px-3 py-2 bg-white text-white dark:bg-gray-800 dark:text-white;" required />
  
        <button type="submit" class="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          ✅ Login
        </button>
      </form>
  
      <p class="text-sm text-gray-500 mt-4 text-center">
        New here?
        <router-link to="/register" class="text-blue-400 hover:underline">Register</router-link>
      </p>
  
      <div v-if="error" class="mt-4 text-red-500 text-sm text-center">{{ error }}</div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import API from '../services/api'
  
  const form = ref({
    username: '',
    password: ''
  })
  
  const error = ref(null)
  const router = useRouter()
  
  async function login() {
    error.value = null
  
    try {
        const res = await API.post('/login', {
        username: form.value.username,
        password: form.value.password
        })

        // Save JWTs
        const access = res.data.access
        const refresh = res.data.refresh

        localStorage.setItem('jwt_access', access)
        localStorage.setItem('jwt_refresh', refresh)
        localStorage.setItem('wallet_username', form.value.username)

        // Set token in headers for future requests
        API.defaults.headers.common['Authorization'] = `Bearer ${access}`

        // Optionally fetch user profile
        const profile = await API.get('/user/profile')


        // Save public key (optional)
        localStorage.setItem('wallet_public', profile.data.user.public_key)
        localStorage.setItem('wallet_role', profile.data.user.role)

        // Redirect to profile
        router.push('/profile').then(() => {
            window.location.reload()  // ✅ Force refresh to reflect UI changes
        }
    )
    } catch (err) {
        console.error("Login error:", err)

        if (err.response) {
            const data = err.response.data
            console.log("Backend response:", data)

            if (data.detail) {
            error.value = data.detail
            } else if (data.non_field_errors) {
            error.value = data.non_field_errors[0]
            } else {
            error.value = data.error || 'Login failed. Please check your credentials.'
            }
        } else if (err.request) {
            console.error("No response received from server")
            error.value = "Server did not respond. Please try again later."
        } else {
            console.error("Unexpected error", err.message)
            error.value = "An unexpected error occurred."
        }           
    }


  }
  </script>
  
  <style scoped>
  </style>
  