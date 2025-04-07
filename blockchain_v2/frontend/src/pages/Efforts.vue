<template>
    <div class="min-w-5xl">
        <div class="px-4 py-6 max-w-5xl mx-auto">
        <h1 class="text-3xl font-bold mb-6">📜 Submitted Efforts</h1>

        <!-- Filters -->
        <div class="mb-4 items-center">
            <input
            v-model="search"
            type="text"
            placeholder="🔍 Search by task or user"
            class="px-3 mr-4 py-2 border rounded w-full sm:w-64"
            />

            <select v-model="selectedType" class="px-3 py-2 border rounded bg-gray-600">
            <option value="">All Types</option>
            <option value="learning">📚 Learning</option>
            <option value="mental">🧠 Mental</option>
            <option value="physical">💪 Physical</option>
            </select>
        </div>

        <!-- Table of efforts -->
            <div v-if="filteredEfforts.length > 0" class="overflow-x-auto rounded shadow max-w-2xl mx-auto">
                <table class="min-w-full table-auto border-collapse">
                <thead class="bg-gray-100 dark:bg-gray-700 text-left text-sm font-semibold">
                    <tr>
                    <th class="px-4 py-2">Task</th>
                    <th class="px-4 py-2">User</th>
                    <th class="px-4 py-2">Type</th>
                    <th class="px-4 py-2">Score</th>
                    <th class="px-4 py-2">Submitted</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                    v-for="effort in filteredEfforts"
                    :key="effort.index"
                    class="text-sm even:bg-gray-50 dark:even:bg-gray-800"
                    >
                    <td class="px-4 py-2">{{ effort.effort_data.task_id }}</td>
                    <td class="px-4 py-2">{{ effort.effort_data.user_id }}</td>
                    <td class="px-4 py-2">
                        <span
                        class="inline-block px-2 py-1 rounded text-xs font-medium"
                        :class="badgeColor(effort.effort_data.effort_type)"
                        >
                        {{ effort.effort_data.effort_type }}
                        </span>
                    </td>
                    <td class="px-4 py-2 font-semibold">{{ effort.effort_data.effort_score }} EFF</td>
                    <td class="px-4 py-2 text-gray-600 dark:text-gray-300">
                        {{ formatTime(effort.timestamp) }}
                    </td>
                    </tr>
                </tbody>
                </table>
            </div>
            <div v-else class="text-gray-500 mt-6 text-center">No efforts found.</div>
        </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import API from '../services/api'
  import { refreshTokenIfNeeded } from '../utils/auth'

  
  const efforts = ref([])
  const search = ref('')
  const selectedType = ref('')
  const loading = ref(true)
  
  onMounted(async () => {
    const ok = await refreshTokenIfNeeded()
    if (!ok) {
        localStorage.clear()
        window.location.href = '/login' // or use router.push('/login') if using Vue Router
        return
    }
    try {
      const res = await API.get('/efforts')
      efforts.value = res.data.chain || []
    } catch (err) {
      console.error('Error fetching efforts:', err)
    } finally {
      loading.value = false
    }
  })
  
  const filteredEfforts = computed(() => {
    return efforts.value.filter(effort => {
      const matchesSearch =
        effort.effort_data.task_id.toLowerCase().includes(search.value.toLowerCase()) ||
        effort.effort_data.user_id.toLowerCase().includes(search.value.toLowerCase())
  
      const matchesType = selectedType.value
        ? effort.effort_data.effort_type === selectedType.value
        : true
  
      return matchesSearch && matchesType
    })
  })
  
  function formatTime(unix) {
    const now = new Date()
    const date = new Date(unix * 1000)
    const diff = Math.round((now - date) / 1000)
  
    if (diff < 60) return `${diff}s ago`
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
    return date.toLocaleDateString()
  }
  
  function badgeColor(type) {
    switch (type) {
      case 'learning':
        return 'bg-blue-100 text-blue-700'
      case 'mental':
        return 'bg-purple-100 text-purple-700'
      case 'physical':
        return 'bg-green-100 text-green-700'
      default:
        return 'bg-gray-100 text-gray-600'
    }
  }
  </script>
  
  <style scoped>
  table {
    border-spacing: 0;
    border-collapse: collapse;
  }
  </style>
  