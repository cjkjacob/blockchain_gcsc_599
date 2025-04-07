<template>
    <div class="min-w-5xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold mb-6 text-center">🌐 Blockchain Explorer</h1>
  
      <div v-if="loading" class="text-center text-gray-500">Loading chain...</div>
  
      <div v-else-if="chain.length === 0" class="text-center text-gray-500">No blocks found.</div>
  
      <div v-else class="space-y-6">
        <div
          v-for="block in chain"
          :key="block.index"
          class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 max-w-lg mx-auto"
        >
          <h2 class="font-semibold text-lg mb-1">🔗 Block #{{ block.index }}</h2>
          <p class="text-sm text-gray-400 mb-2">⏱ {{ formatDate(block.timestamp) }}</p>
  
          <div class="text-sm space-y-1">
            <p><strong>🧑‍🎓 User:</strong> {{ block.effort_data.user_id }}</p>
            <p><strong>📝 Task:</strong> {{ block.effort_data.task_id }}</p>
            <p><strong>📚 Type:</strong> {{ block.effort_data.effort_type }}</p>
            <p><strong>📈 Score:</strong> {{ block.effort_data.effort_score }} EFF</p>
            <p><strong>✅ Validated By:</strong> {{ block.validated_by }}</p>
          </div>
  
          <details class="mt-3 text-xs text-gray-400">
            <summary class="cursor-pointer">🔐 Signatures & Hashes</summary>
            <div class="mt-2 break-all">
              <p><strong>Public Hash:</strong> {{ block.hash }}</p>
              <p><strong>Prev Hash:</strong> {{ block.previous_hash }}</p>
              <p><strong>User Sig:</strong> {{ block.proof?.user_signature }}</p>
              <p><strong>Validator Sig:</strong> {{ block.proof?.validator_signature }}</p>
            </div>
          </details>
        </div>
      </div>
    </div>

  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import API from '../services/api'
  import { refreshTokenIfNeeded } from '../utils/auth'
  
  const chain = ref([])
  const loading = ref(true)
  
  onMounted(async () => {
    const ok = await refreshTokenIfNeeded()
    if (!ok) {
      localStorage.clear()
      window.location.href = '/login'
      return
    }
    try {
      const res = await API.get('/chain')
      chain.value = res.data.chain.reverse()
    } catch (err) {
      console.error('Failed to fetch chain:', err)
    } finally {
      loading.value = false
    }
  })
  
  function formatDate(timestamp) {
    const date = new Date(timestamp * 1000)
    return date.toLocaleString()
  }
  </script>
  