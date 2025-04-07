<template>
    <div class="px-4 py-6 max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold mb-6 text-center min-w-5xl">🚀 Submit Effort</h1>
  
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
          <label class="block mb-1 font-medium">Evidence File URL</label>
          <input v-model="form.file_url" type="text" placeholder="https://example.com/myfile.pdf" class="input w-full border rounded px-3 py-2" required />
        </div>
  
        <div>
          <label class="block mb-1 font-medium">Effort Score</label>
          <input v-model.number="form.effort_score" type="number" min="0" class="input w-full border rounded px-3 py-2" required />
        </div>
  
        <div>
          <label class="block mb-1 font-medium">Validator ID</label>
          <input v-model="form.validator_id" type="text" class="input w-full border rounded px-3 py-2" required />
        </div>
  
        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          ✅ Submit Effort
        </button>
      </form>
  
      <div v-if="error" class="text-red-500 mt-4 text-sm">{{ error }}</div>
      <div v-if="message" class="text-green-600 mt-4 text-sm">{{ message }}</div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import API from '../services/api'
  import { refreshTokenIfNeeded } from '../utils/auth'
  import elliptic from 'elliptic'
  import { Buffer } from 'buffer'
  import stringify from 'json-stable-stringify'
  
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
  
  async function submitEffort() {
    message.value = null
    error.value = null
    const ok = await refreshTokenIfNeeded()
    if (!ok) {
      error.value = 'Session expired. Please log in again.'
      return
    }

  
    const privateKey = localStorage.getItem('wallet_private')
    const key = ec.keyFromPrivate(privateKey, 'hex')
    const publicKey = key.getPublic(false, 'hex') // includes '04' prefix
    // const publicKey = localStorage.getItem('wallet_public')
    // let publicKey = localStorage.getItem('wallet_public')
    // if (publicKey.startsWith('04')) {
    //   publicKey = publicKey.slice(2)
    // }
    
    const validatorPrivate = localStorage.getItem('validator_private')
    // const validatorPublic = localStorage.getItem('validator_public')
    let validatorPublic = localStorage.getItem('validator_public')
    if (validatorPublic.startsWith('04')) {
      validatorPublic = validatorPublic.slice(2)
    }
    const username = localStorage.getItem('wallet_username')  

    if (!privateKey || !publicKey || !validatorPrivate || !validatorPublic) {
      error.value = 'Wallet or validator keys not found in local storage.'
      return
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

    // function deepSort(obj) {
    //   if (Array.isArray(obj)) {
    //     return obj.map(deepSort)
    //   } else if (obj !== null && typeof obj === 'object') {
    //     return Object.keys(obj).sort().reduce((result, key) => {
    //       result[key] = deepSort(obj[key])
    //       return result
    //     }, {})
    //   }
    //   return obj
    // }

    const canonicalJSON = stringify(effort_data) // deep key sort
    console.log("canonical payload:", canonicalJSON)
    const encoded = new TextEncoder().encode(canonicalJSON)
    const digestBuffer = await crypto.subtle.digest('SHA-256', encoded)
    const digest = Buffer.from(digestBuffer)
    console.log("frontend digest", digest.toString('hex'))
  
    // const key = ec.keyFromPrivate(privateKey, 'hex')
    const validatorKey = ec.keyFromPrivate(validatorPrivate, 'hex')
  
    const sig = key.sign(digest, { canonical: true })    
    const userSignature =
    sig.r.toArrayLike(Buffer, 'be', 32).toString('hex') +
    sig.s.toArrayLike(Buffer, 'be', 32).toString('hex')


    const validatorSig = validatorKey.sign(digest)
    const validatorSignature = validatorSig.r.toArrayLike(Buffer, 'be', 32).toString('hex') + validatorSig.s.toArrayLike(Buffer, 'be', 32).toString('hex')

  
    try {
      const res = await API.post('/submit-effort', {
        effort_data,
        user_signature: userSignature,
        user_public_key: publicKey,
        validator_id: form.value.validator_id,
        validator_signature: validatorSignature,
        validator_public_key: validatorPublic
      })
  
      message.value = res.data.message || 'Effort submitted successfully!'
      console.log({
        effort_data,
        user_signature: userSignature,
        user_public_key: publicKey,
        validator_id: form.value.validator_id,
        validator_signature: validatorSignature,
        validator_public_key: validatorPublic
    })

    } catch (err) {
        console.error('Submission failed:', err)

        if (err.response) {
            console.log("Backend Response:", err.response.data)
            error.value = err.response.data?.error || JSON.stringify(err.response.data)
        } else {
            error.value = err.message || 'Submission failed.'
        }
    }
  }
  </script>
  
  <style scoped>
  input, select {
    background-color: white;
    color: black;
  }
  </style>
  