import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(),tailwindcss()],
  server: {
      host: true,       // 👈 this ensures 0.0.0.0 binding
      port: 5173,
      strictPort: true
    },
})
