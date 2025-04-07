<template>
    <div class="max-w-3xl mx-auto p-6">
        <h1 class="text-2xl font-bold mb-10">📝 Register</h1>

        <form @submit.prevent="register" class="space-y-4">
        <input v-model="form.username" type="text" placeholder="Username" class="input w-full border rounded px-3 py-2 bg-white text-black dark:bg-gray-800 dark:text-white" required />
        <input v-model="form.email" type="email" placeholder="Email" class="input w-full border rounded px-3 py-2 bg-white text-black dark:bg-gray-800 dark:text-white" required />
        <input v-model="form.password" type="password" placeholder="Password" class="input w-full border rounded px-3 py-2 bg-white text-black dark:bg-gray-800 dark:text-white" required />
        <input v-model="form.confirm" type="password" placeholder="Confirm Password" class="input w-full border rounded px-3 py-2 bg-white text-black dark:bg-gray-800 dark:text-white" required />

        <select v-model="form.role" class="input w-full border rounded px-3 py-2 bg-white text-black dark:bg-gray-800 dark:text-white" required>
            <option disabled value="">Select Role</option>
            <option value="student">Student</option>
            <option value="validator">Validator</option>
        </select>

        <button type="submit" class="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            🚀 Create Account
        </button>
        </form>

        <p class="text-sm text-gray-500 mt-4 text-center">
        Already registered?
        <router-link to="/login" class="text-blue-400 hover:underline">Login here</router-link>
        </p>

        <div v-if="error" class="mt-4 text-red-500 text-sm text-center">{{ error }}</div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import API from '../services/api'
import elliptic from 'elliptic'
import { useRouter } from 'vue-router'

const EC = elliptic.ec
const ec = new EC('secp256k1')
const router = useRouter()
const error = ref(null)

const form = ref({
username: '',
email: '',
password: '',
confirm: '',
role: ''
})

function downloadPrivateKey(privateKey, username) {
  const blob = new Blob([privateKey], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)

  const a = document.createElement('a')
  a.href = url
  a.download = `${username}_proof_of_effort_private_key.txt`
  a.click()

  URL.revokeObjectURL(url)
}


async function register() {
  if (form.value.password !== form.value.confirm) {
    error.value = "Passwords do not match."
    return
  }

  try {
    const key = ec.genKeyPair()
    const privateKey = key.getPrivate('hex')
    const publicKey = key.getPublic('hex')

    const payload = {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      public_key: publicKey,
      role: form.value.role
    }

    await API.post('/register', payload)

    // Save to localStorage
    localStorage.setItem('wallet_private', privateKey)
    localStorage.setItem('wallet_public', publicKey)
    localStorage.setItem('wallet_username', payload.username)

    // Trigger file download for private key
    downloadPrivateKey(privateKey, payload.username)

    // Redirect
    router.push('/profile').then(() => {
      window.location.reload()
    })
  } catch (err) {
    console.error("Registration error:", err)
    if (err.response?.data) {
      error.value = Object.values(err.response.data).flat().join(' ') || 'Registration failed.'
    } else {
      error.value = 'Registration failed.'
    }
  }
}

</script>

<style scoped>
</style>
  