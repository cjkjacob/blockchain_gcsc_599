import { createRouter, createWebHistory } from 'vue-router'
import Home from './../pages/Home.vue'
import Profile from './../pages/Profile.vue'
import Register from './../pages/Register.vue'
import Login from './../pages/Login.vue'
import Submit from './../pages/Submit.vue'
import Chain from './../pages/Chain.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/register', component: Register },
    { path: '/login', component: Login },
    { path: '/profile', component: Profile },
    { path: '/submit', component: Submit },
    { path: '/chain', component: Chain },
  ]
})
