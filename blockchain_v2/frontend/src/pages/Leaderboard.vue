<template>
    <div class="px-4 py-6 min-w-5xl mx-auto">
      <h1 class="text-3xl font-bold mb-6 text-center">🏆 Leaderboard</h1>
  
      <div v-if="loading" class="text-center text-gray-500">Loading leaderboard...</div>
      <div v-else-if="leaders.length === 0" class="text-center text-gray-500">No data yet.</div>
  
      <div v-else class="bg-white dark:bg-gray-800 shadow rounded-lg max-w-2xl mx-auto overflow-x-auto">
        <table class="min-w-full table-auto text-sm sm:text-base">
          <thead class="bg-gray-100 dark:bg-gray-700 font-semibold">
            <tr>
              <th class="px-4 py-2">#</th>
              <th class="px-4 py-2">Username</th>
              <th class="px-4 py-2">Total Score</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(user, index) in leaders"
              :key="user.username"
              class="even:bg-gray-50 dark:even:bg-gray-900"
            >
              <td class="px-4 py-2">{{ index + 1 }}</td>
              <td class="px-4 py-2">{{ user.username }}</td>
              <td class="px-4 py-2 font-semibold">{{ user.total_score }} EFF</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import API from '../services/api'
  import { refreshTokenIfNeeded } from '../utils/auth'
  
  const leaders = ref([])
  const loading = ref(true)
  
  onMounted(async () => {
    const ok = await refreshTokenIfNeeded()
    if (!ok) {
      localStorage.clear()
      window.location.href = '/login'
      return
    }
  
    try {
      const res = await API.get('/leaderboard')
      leaders.value = res.data
    } catch (err) {
      console.error('Failed to fetch leaderboard', err)
    } finally {
      loading.value = false
    }
  })
  </script>
  