<template>
  <div class="px-4 py-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6 text-center">👤 My Profile</h1>

    <div v-if="loading" class="text-gray-500 text-center">Loading...</div>

    <div v-else-if="profile.user" class="space-y-10">

      <!-- Wallet Info -->
      <section class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">🔑 Wallet Info</h2>
        <div class="grid gap-4 md:grid-cols-2 text-sm sm:text-base">
          <p><span class="font-medium">Username:</span> {{ profile.user.username }}</p>
          <p><span class="font-medium">Role:</span> {{ profile.user.role }}</p>
          <p class="md:col-span-2 break-all">
            <span class="font-medium">Public Key:</span> {{ profile.user.public_key }}
          </p>
          <p v-if="profile.user.role != 'validator'" class="text-green-600 font-semibold md:col-span-2 mt-2">
            🎁 Token Balance: {{ profile.token_balance }} EFF
          </p>
        </div>
      </section>

      <!-- Effort Submissions -->
      <section  v-if="profile.user.role != 'validator'" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">📚 Effort Submissions</h2>
        <div v-if="profile.efforts.length === 0" class="text-gray-500">No submissions yet.</div>
        <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
          <div v-for="effort in profile.efforts" :key="effort.index" class="py-4 text-sm sm:text-base">
            <div class="grid md:grid-cols-2 gap-2">
              <p><span class="font-medium">Task:</span> {{ effort.effort_data.task_id }}</p>
              <p><span class="font-medium">Score:</span> {{ effort.effort_data.effort_score }} EFF</p>
              <p class="md:col-span-2"><span class="font-medium">Submitted:</span> {{ formatDate(effort.timestamp) }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Validator Dashboard -->
      <section v-if="profile.user.role === 'validator'">
        <!-- Upload Validator Private Key -->
        <div v-if="!hasValidatorKey" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
          <h2 class="text-xl font-semibold mb-4">🔐 Upload Validator Private Key</h2>
          <p class="text-sm text-gray-500 mb-2">
            This is needed to approve efforts. Your key will only be stored locally in your browser.
          </p>
          <input
            type="file"
            accept=".txt,.json"
            @change="handleKeyUpload"
            class="block w-full text-sm text-gray-700 dark:text-gray-300 file:mr-4 file:py-2 file:px-4 file:border file:rounded file:text-sm file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <p v-if="uploadMessage" class="mt-2 text-green-600 text-sm">{{ uploadMessage }}</p>
          <p v-if="uploadError" class="mt-2 text-red-500 text-sm">{{ uploadError }}</p>
        </div>
        <div v-if="hasValidatorKey" class="mt-4 mb-4">
          <label class="font-medium text-sm">🔑 Validator Private Key:</label>
          <textarea
            v-if="showPrivate"
            readonly
            class="w-full p-2 mt-2 border rounded bg-gray-600 text-sm text-white"
            rows="3"
            :value="validatorKeyDisplay"
          />
          <button @click="togglePrivate" class="text-white hover:underline text-sm mt-1">
            {{ showPrivate ? '🙈 Hide' : '👁️ Show' }} Validator Key
          </button>
          <button @click="copyToClipboard(validatorKeyDisplay)" class="text-white hover:underline text-sm ml-4" v-if="showPrivate">
            📋 Copy
          </button>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">⏳ Pending Efforts</h2>
          <div v-if="pending.length === 0" class="text-gray-500">No efforts to validate.</div>
          <div v-else class="space-y-4">
            <div v-for="effort in pending" :key="effort.id" class="p-4 border rounded bg-gray-50 dark:bg-gray-700">
              <p><strong>User:</strong> {{ effort.submitted_by }}</p>
              <p><strong>Task:</strong> {{ effort.effort_data.task_id }}</p>
              <p><strong>Score:</strong> {{ effort.effort_data.effort_score }}</p>
              <p><strong>Submitted:</strong> {{ formatDate(effort.submitted_at) }}</p>
              <p v-if="effort.effort_data.submission?.file_url">
                <strong>Evidence:</strong>
                <a
                  :href="effort.effort_data.submission.file_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-blue-600 hover:underline"
                >
                  View File
                </a>
              </p>
              <div class="mt-3 space-y-2">
                <textarea
                  v-model="rejectReasons[effort.id]"
                  rows="2"
                  placeholder="Enter reason for rejection..."
                  class="w-full text-sm border rounded p-2"
                ></textarea>

                <div class="flex gap-4">
                  <button
                    @click="approve(effort.id)"
                    :disabled="!hasValidatorKey"
                    class="px-4 py-1 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
                  >
                    ✅ Approve
                  </button>
                  <button
                    @click="reject(effort.id)"
                    :disabled="!rejectReasons[effort.id]"
                    class="px-4 py-1 bg-red-600 text-white rounded hover:bg-red-700 disabled:opacity-50"
                  >
                    ❌ Reject
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mt-6">
          <h2 class="text-xl font-semibold mb-4">🚫 Rejected Efforts</h2>
          <div v-if="rejected.length === 0" class="text-gray-500">No rejections recorded.</div>
          <div v-else class="space-y-3 text-sm">
            <div v-for="effort in rejected" :key="effort.id" class="p-3 border rounded bg-gray-100 dark:bg-gray-700">
              <p><strong>User:</strong> {{ effort.user_id }}</p>              
              <p><strong>Task:</strong> {{ effort.task_id }}</p>
              <p v-if="effort.file_url">
                <strong>Evidence:</strong>
                <a
                  :href="effort.file_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-blue-600 hover:underline"
                >
                  View File
                </a>
              </p>
              <p class="text-red-500"><strong>Rejected:</strong> {{ formatDate(effort.submitted_at) }}</p>
              <p><strong>Reason:</strong> {{ effort.reason }}</p>            
            </div>
          </div>
        </div>
      </section>

    </div>

    <div v-else class="text-center text-red-500">Failed to load profile data.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import API from '../services/api'
import { refreshTokenIfNeeded } from '../utils/auth'
import elliptic from 'elliptic'
import stringify from 'json-stable-stringify'
import { Buffer } from 'buffer'


const EC = elliptic.ec
const ec = new EC('secp256k1')
const showPrivate = ref(false)
const validatorKeyDisplay = ref(localStorage.getItem('validator_private') || '')
const profile = ref({})
const loading = ref(true)
const pending = ref([])
const rejected = ref([])
const rejectReasons = ref({})
const uploadMessage = ref('')
const uploadError = ref('')
const hasValidatorKey = ref(!!localStorage.getItem('validator_private'))

function togglePrivate() {
  showPrivate.value = !showPrivate.value
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    uploadMessage.value = 'Copied to clipboard!'
    setTimeout(() => (uploadMessage.value = ''), 1500)
  }).catch(() => {
    uploadError.value = 'Failed to copy.'
    setTimeout(() => (uploadError.value = ''), 1500)
  })
}

onMounted(async () => {
  const ok = await refreshTokenIfNeeded()
  if (!ok) {
    localStorage.clear()
    window.location.href = '/login'
    return
  }

  try {
    const res = await API.get('/user/profile')
    profile.value = res.data

    if (profile.value.user.role === 'validator') {
      const p = await API.get('/validator/pending-efforts')
      const r = await API.get('/validator/rejected-efforts')
      pending.value = p.data
      rejected.value = r.data
    }
  } catch (err) {
    console.error('Failed to load profile', err)
  } finally {
    loading.value = false
  }
  if(!hasValidatorKey){
    uploadMessage.value = 'Please upload your validator private key.'
  }
})

function handleKeyUpload(event) {
  uploadMessage.value = ''
  uploadError.value = ''
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    try {
      const text = reader.result.trim()
      // Try parsing as JSON or plain text
      let privateKey = text
      if (text.startsWith('{')) {
        const parsed = JSON.parse(text)
        privateKey = parsed.privateKey || parsed.validator_private || parsed.private_key
      }

      if (!privateKey || privateKey.length !== 64) {
        uploadError.value = 'Invalid key format. Expected 64-character hex string.'
        return
      }

      // Try generating key to validate
      const key = ec.keyFromPrivate(privateKey, 'hex')
      const pub = key.getPublic(false, 'hex')
      localStorage.setItem('validator_public', pub.startsWith('04') ? pub.slice(2) : pub)
      localStorage.setItem('validator_private', privateKey)
      validatorKeyDisplay.value = privateKey
      hasValidatorKey.value = true

      uploadMessage.value = 'Private key uploaded and saved locally.'
      hasValidatorKey.value = true
    } catch (err) {
      console.error('Key upload error:', err)
      uploadError.value = 'Failed to parse or store key. Check the file format.'
    }
  }

  reader.readAsText(file)
}

async function approve(id) {
  if (!hasValidatorKey.value) {
    alert('Validator private key is missing. Please upload it before approving.')
    return
  }

  const ok = await refreshTokenIfNeeded()
  if (!ok) return

  const effort = pending.value.find(e => e.id === id)
  if (!effort) return

  try {
    const validatorPrivate = localStorage.getItem('validator_private')
    const validatorKey = ec.keyFromPrivate(validatorPrivate, 'hex')

    const canonical = stringify(effort.effort_data)
    const encoded = new TextEncoder().encode(canonical)
    const digestBuffer = await crypto.subtle.digest('SHA-256', encoded)
    const digest = Buffer.from(digestBuffer)

    const sig = validatorKey.sign(digest, { canonical: true })
    const validatorSignature =
      sig.r.toArrayLike(Buffer, 'be', 32).toString('hex') +
      sig.s.toArrayLike(Buffer, 'be', 32).toString('hex')

    await API.post(`/validator/approve-effort/${id}`, {
      validator_signature: validatorSignature
    })

    pending.value = pending.value.filter(e => e.id !== id)
  } catch (err) {
    console.error('Approve failed:', err)
  }
}


async function reject(id) {
  const reason = rejectReasons.value[id] || ''
  if (!reason.trim()) return

  const ok = await refreshTokenIfNeeded()
  if (!ok) return

  try {
    await API.post(`/validator/reject-effort/${id}`, { reason })
    pending.value = pending.value.filter(e => e.id !== id)
    const r = await API.get('/validator/rejected-efforts')
    rejected.value = r.data
  } catch (err) {
    console.error('Reject failed:', err)
  }
}

function formatDate(ts) {
  return new Date(ts * 1000 || ts).toLocaleString()
}
</script>

