<template>
  <div class="px-4 py-6 min-w-5xl mx-auto">
    <h1 class="text-3xl font-bold mb-6 text-center">🚀 Submit Effort</h1>

    <form @submit.prevent="submitEffort" class="space-y-6 max-w-md mx-auto">
      <div>
        <label class="block mb-1 font-medium">Task ID</label>
        <input v-model="form.task_id" type="text" class="input w-full border rounded px-3 py-2" required />
      </div>

      <div>
        <label class="block mb-1 font-medium">Effort Type</label>
        <select v-model="form.effort_type" class="input w-full border rounded px-3 py-2">
          <option value="learning">Learning</option>
          <option value="mental">Mental</option>
          <option value="physical">Physical</option>
        </select>
      </div>

      <div>
        <label class="block mb-1 font-medium">Evidence File</label>
        <input
          type="file"
          ref="fileInputRef"
          @change="handleFileUpload"
          accept="image/*,.pdf,.doc,.docx"
          class="input w-full border rounded px-3 py-2 bg-gray-800 hover:bg-gray-500 cursor-pointer"
        />
        <p class="text-xs text-gray-500 mt-1">Accepted formats: image, PDF, DOC</p>
        <div v-if="form.file_url" class="text-sm text-green-600 mt-1">✔️ File uploaded</div>
      </div>

      <div>
        <label class="block mb-1 font-medium">Effort Score</label>
        <input v-model.number="form.effort_score" type="number" min="0" class="input w-full border rounded px-3 py-2" required />
      </div>

      <div>
        <label class="block mb-1 font-medium">Validator ID</label>
        <input v-model="form.validator_id" type="text" class="input w-full border rounded px-3 py-2" required />
      </div>

      <button type="submit" :disabled="!form.file_url" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50">
        ✅ Submit Effort
      </button>
    </form>

    <div v-if="error" class="text-red-500 mt-4 text-sm">{{ error }}</div>
    <div v-if="message" class="text-green-600 mt-4 text-sm">{{ message }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import API from '../services/api'
import { refreshTokenIfNeeded } from '../utils/auth'
import elliptic from 'elliptic'
import { Buffer } from 'buffer'
import stringify from 'json-stable-stringify'
import { useRouter } from 'vue-router'

const EC = elliptic.ec
const ec = new EC('secp256k1')

const form = ref({
  task_id: '',
  effort_type: 'learning',
  file_url: '',
  effort_score: 0,
  validator_id: ''
})

const message = ref(null)
const error = ref(null)
const fileInputRef = ref(null)
const router = useRouter()

const role = localStorage.getItem('wallet_role')
const username = localStorage.getItem('wallet_username')
const privateKey = localStorage.getItem('wallet_private')

onMounted(() => {
  if (!privateKey) {
    error.value = 'Private key not found. Please restore your wallet.'
    setTimeout(() => {
      router.push('/wallet')
    }, 2500)
  }
})

async function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  const ok = await refreshTokenIfNeeded()
  if (!ok) {
    error.value = 'Session expired. Please log in again.'
    return
  }

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await API.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    form.value.file_url = res.data.file_url
  } catch (err) {
    console.error('File upload failed:', err)
    error.value = 'File upload failed. Please try again.'
  }
}

async function submitEffort() {
  message.value = null
  error.value = null

  const ok = await refreshTokenIfNeeded()
  if (!ok) {
    error.value = 'Session expired. Please log in again.'
    return
  }

  const key = ec.keyFromPrivate(privateKey, 'hex')
  let publicKey = key.getPublic(false, 'hex')
  if (publicKey.startsWith('04')) {
    publicKey = publicKey.slice(2)
  }

  const effort_data = {
    user_id: username,
    task_id: form.value.task_id,
    effort_type: form.value.effort_type,
    submission: {
      file_url: form.value.file_url,
      submitted_at: new Date().toISOString()
    },
    effort_score: form.value.effort_score
  }

  const canonical = stringify(effort_data)
  const digestBuffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(canonical))
  const digest = Buffer.from(digestBuffer)

  let userSignature = null
  if (role === 'student') {
    const sig = key.sign(digest, { canonical: true })
    userSignature =
      sig.r.toArrayLike(Buffer, 'be', 32).toString('hex') +
      sig.s.toArrayLike(Buffer, 'be', 32).toString('hex')
  }

  try {
    const res = await API.post('/submit-effort', {
      effort_data,
      user_signature: userSignature,
      user_public_key: publicKey,
      validator_id: form.value.validator_id
    })
    message.value = res.data.message || 'Effort queued successfully!'
    form.value = {
      task_id: '',
      effort_type: 'learning',
      file_url: '',
      effort_score: 0,
      validator_id: ''
    }
    if (fileInputRef.value) {
      fileInputRef.value.value = '' 
    }
  } catch (err) {
    console.error('Submission failed:', err)
    error.value = err.response?.data?.error || JSON.stringify(err.response?.data || err.message || 'Unknown error')
  }
}
</script>

<style scoped>
input, select {
  background-color: white;
  color: black;
}
</style>