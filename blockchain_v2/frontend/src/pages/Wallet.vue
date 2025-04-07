<template>
  <div class="min-w-5xl mx-auto px-4 py-6">
    <div class="max-w-xl mx-auto">
      <h1 class="text-3xl font-bold mb-6 text-center">🔐 My Wallet</h1>

      <!-- ⚠️ Warning if private key is missing -->
      <div
        v-if="isMissingPrivateKey"
        class="bg-yellow-100 text-yellow-800 p-4 rounded text-sm mb-6 border border-yellow-300"
      >
        ⚠️ Your private key is not stored locally. You won't be able to submit efforts until you restore your wallet.
        <br />
        Please <strong>upload your backup</strong> below.
      </div>

      <div class="space-y-4 p-4 rounded shadow-md">
        <div>
          <label class="font-medium">Username:</label>
          <div class="text-white mt-2 bg-gray-600 max-w-sm mx-auto rounded">{{ username || 'Not set' }}</div>
        </div>

        <div>
          <label class="font-medium">Public Key:</label>
          <textarea
            readonly
            class="w-full p-2 mt-2 border rounded bg-gray-600 text-sm text-white"
            rows="3"
            :value="publicKey"
          />
          <button @click="copyToClipboard(publicKey)" class="text-white hover:underline text-sm mt-1">📋 Copy</button>
        </div>

        <div>
          <label class="font-medium">Private Key:</label>
          <textarea
            v-if="showPrivate"
            readonly
            class="w-full p-2 mt-2 border rounded bg-gray-600 text-sm text-white"
            rows="3"
            :value="privateKey"
          />
          <button @click="togglePrivate" class="text-white hover:underline text-sm mt-1">
            {{ showPrivate ? '🙈 Hide' : '👁️ Show' }} Private Key
          </button>
          <button @click="copyToClipboard(privateKey)" class="text-white hover:underline text-sm ml-4" v-if="showPrivate">📋 Copy</button>
        </div>

        <div class="pt-4">
          <button @click="downloadBackup" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
            💾 Download Wallet Backup
          </button>
        </div>

        <!-- 🔁 Restore from uploaded TXT -->
        <div v-if="isMissingPrivateKey" class="pt-4 border-t mt-6">
          <label class="font-medium block mb-2">🔁 Restore Wallet from Backup File (.txt):</label>
          <input
            type="file"
            accept=".txt"
            @change="handleFileUpload"
            class="block w-full border px-3 py-2 rounded bg-gray-800 text-white hover:bg-gray-500 cursor-pointer text-sm"
          />
        </div>
      </div>

      <div v-if="message" class="text-green-600 mt-4 text-sm text-center">{{ message }}</div>
      <div v-if="error" class="text-red-500 mt-4 text-sm text-center">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { refreshTokenIfNeeded } from '../utils/auth'
import elliptic from 'elliptic'

const EC = elliptic.ec
const ec = new EC('secp256k1')

const publicKey = localStorage.getItem('wallet_public') || ''
const localPrivateKey = localStorage.getItem('wallet_private') || ''
const username = localStorage.getItem('wallet_username') || ''
const privateKey = ref(localPrivateKey)
const isMissingPrivateKey = computed(() => !privateKey.value)
const showPrivate = ref(false)
const message = ref(null)
const error = ref(null)

onMounted(async () => {
  const ok = await refreshTokenIfNeeded()
  if (!ok) {
    localStorage.clear()
    window.location.href = '/login'
    return
  }
})

function togglePrivate() {
  showPrivate.value = !showPrivate.value
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    message.value = 'Copied to clipboard!'
    setTimeout(() => (message.value = null), 1500)
  }).catch(() => {
    error.value = 'Failed to copy.'
    setTimeout(() => (error.value = null), 1500)
  })
}

function downloadBackup() {
  const blob = new Blob(
    [JSON.stringify({
      username,
      publicKey,
      privateKey: privateKey.value  // ✅ Extract the string
    }, null, 2)],
    { type: 'application/json' }
  )

  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${username || 'user'}_wallet_backup.json`
  a.click()
  URL.revokeObjectURL(url)
}


function handleFileUpload(event) {
  message.value = null
  error.value = null

  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const raw = e.target.result.trim()

      if (!raw || raw.length !== 64) {
        throw new Error('Invalid private key format')
      }

      const key = ec.keyFromPrivate(raw, 'hex')
      const pubKey = key.getPublic(false, 'hex')

      localStorage.setItem('wallet_private', raw)
      localStorage.setItem('wallet_public', pubKey.startsWith('04') ? pubKey.slice(2) : pubKey)

      message.value = '✅ Wallet restored successfully!'
      isMissingPrivateKey.value = false

      // 🔁 Reload to reflect the restored key across the app
      setTimeout(() => {
        window.location.reload()
      }, 1000)
    } catch (err) {
      console.error(err)
      error.value = '❌ Failed to restore wallet. Make sure it’s a valid .txt file with your private key.'
    }
  }

  reader.readAsText(file)
}




</script>

<style scoped>
textarea {
  font-family: monospace;
}
</style>