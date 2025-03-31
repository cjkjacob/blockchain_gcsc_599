<template>
  <div class="px-4 py-6 max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold mb-6 text-center md:text-left">👤 My Profile</h1>

    <div v-if="loading" class="text-gray-500 text-center">Loading...</div>

    <div v-else-if="profile.user" class="space-y-8">
      <!-- Wallet Info -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">🔑 Wallet Info</h2>
        <div class="grid gap-4 md:grid-cols-2 text-sm sm:text-base">
          <p><span class="font-medium">Username:</span> {{ profile.user.username }}</p>
          <p><span class="font-medium">Role:</span> {{ profile.user.role }}</p>
          <p class="md:col-span-2 break-all">
            <span class="font-medium">Public Key:</span> {{ profile.user.public_key }}
          </p>
          <p class="text-green-600 font-semibold md:col-span-2 mt-2">
            🎁 Token Balance: {{ profile.token_balance }} EFF
          </p>
        </div>
      </div>

      <!-- Efforts -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">📚 Effort Submissions</h2>
        <div v-if="profile.efforts.length === 0" class="text-gray-500">No submissions yet.</div>
        <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
          <div
            v-for="effort in profile.efforts"
            :key="effort.index"
            class="py-4 text-sm sm:text-base"
          >
            <div class="grid md:grid-cols-2 gap-2">
              <p><span class="font-medium">Task:</span> {{ effort.effort_data.task_id }}</p>
              <p><span class="font-medium">Score:</span> {{ effort.effort_data.effort_score }} EFF</p>
              <p class="md:col-span-2"><span class="font-medium">Submitted:</span> {{ formatDate(effort.timestamp) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center text-red-500">Failed to load profile data.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import API from '../services/api'

const profile = ref({})
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await API.get('/user/profile')
    profile.value = res.data
  } catch (err) {
    console.error('Failed to load profile', err)
  } finally {
    loading.value = false
  }
})

function formatDate(timestamp) {
  const date = new Date(timestamp * 1000)
  return date.toLocaleString()
}
</script>
