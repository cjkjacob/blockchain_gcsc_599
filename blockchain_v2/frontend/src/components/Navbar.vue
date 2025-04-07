<template>
    <nav class="bg-gray-900 text-white px-6 py-4 shadow">
        <div class="max-w-7xl mx-auto flex items-center justify-between">
        <!-- Left: Logo -->
        <div>
            <router-link to="/" class="text-lg text-white font-bold hover:text-teal-400">
            🧱 Proof of Effort
            </router-link>
        </div>

        <!-- Right: Nav Links -->
        <div class="flex space-x-6">
            <template v-if="!isLoggedIn">
            <router-link to="/register" class="hover:text-teal-400" :class="isActive('/register')">🆕 Register</router-link>
            <router-link to="/login" class="hover:text-teal-400" :class="isActive('/login')">🔑 Login</router-link>
            </template>

            <template v-else>
            
            <router-link
            v-if="role === 'validator'"
            to="/profile"
            class="text-purple-100 font-semibold hover:text-purple-800"
            >
            🧑‍⚖️ Validator Dashboard
            </router-link>
            <router-link to="/leaderboard" class="hover:text-purple-800" >🏆 Leaderboard </router-link>
            <router-link v-if="role != 'validator'" to="/profile" class="hover:text-teal-400" :class="isActive('/profile')">👤 Profile</router-link>
            <router-link v-if="role != 'validator'" to="/submit" class="hover:text-teal-400" :class="isActive('/submit')">📝 Submit</router-link>
            <router-link to="/chain" class="hover:text-teal-400" :class="isActive('/chain')">⛓️ Chain</router-link>
            <router-link v-if="role != 'validator'" to="/wallet" class="hover:text-teal-400" :class="isActive('/wallet')">🔐 Wallet</router-link>
            <router-link to="/efforts" class="hover:text-teal-400" :class="isActive('/efforts')">📜 Efforts</router-link>
            <button @click="logout" class="hover:text-red-400">Logout</button>
            </template>
        </div>
        </div>
    </nav>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { logoutUser } from '../utils/auth'
import { ref, computed, onMounted } from 'vue'
import API from '../services/api'

const router = useRouter()
const route = useRoute()

const role = ref(null)

  
onMounted(() => {
  role.value = localStorage.getItem('wallet_role')
})

const isLoggedIn = computed(() => !!localStorage.getItem('jwt_access'))

function logout() {
  console.log("Logout triggered")  // ✅ Check if this logs
  logoutUser(router)
}

function isActive(path) {
    return route.path === path ? 'text-teal-400 font-semibold' : ''
}
</script>

<style scoped>
button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
}
</style>
    