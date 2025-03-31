<template>
    <div class="max-w-xl mx-auto p-6">
      <h1 class="text-2xl font-bold mb-4">🔐 Wallet Generator</h1>
  
      <div class="space-y-4">
        <button @click="generateWallet"
                class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          ✨ Generate New Wallet
        </button>
  
        <div v-if="wallet" class="bg-white dark:bg-gray-800 rounded shadow p-4">
          <p><strong>Public Key:</strong></p>
          <p class="break-all text-sm mb-3 text-green-500">{{ wallet.publicKey }}</p>
          <p><strong>Private Key:</strong></p>
          <p class="break-all text-sm text-yellow-400">{{ wallet.privateKey }}</p>
  
          <p class="mt-3 text-gray-400 text-xs">
            Your private key is stored only in your browser (localStorage).
            Keep it safe!
          </p>
        </div>
  
        <div v-if="storedKey" class="text-sm mt-6">
          <p class="mb-1 text-gray-400">🔒 Stored Wallet:</p>
          <p><strong>Public:</strong> {{ storedKey.public }}</p>
          <p><strong>Private:</strong> {{ storedKey.private }}</p>
          <button @click="clearWallet" class="mt-2 text-red-500 text-xs hover:underline">Clear Stored Wallet</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { EC } from 'elliptic'
  
  const ec = new EC('secp256k1')
  const wallet = ref(null)
  const storedKey = ref(null)
  
  function generateWallet() {
    const key = ec.genKeyPair()
    const privateKey = key.getPrivate('hex')
    const publicKey = key.getPublic('hex')
  
    wallet.value = {
      privateKey,
      publicKey
    }
  
    localStorage.setItem('wallet_private', privateKey)
    localStorage.setItem('wallet_public', publicKey)
  
    storedKey.value = {
      private: privateKey,
      public: publicKey
    }
  }
  
  function clearWallet() {
    localStorage.removeItem('wallet_private')
    localStorage.removeItem('wallet_public')
    storedKey.value = null
  }
  
  onMounted(() => {
    const pk = localStorage.getItem('wallet_private')
    const pub = localStorage.getItem('wallet_public')
    if (pk && pub) {
      storedKey.value = { private: pk, public: pub }
    }
  })
  </script>
  