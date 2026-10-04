import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],

  server: {
    host: '127.0.0.1',
    port: 5173,

    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/wenze': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/finance': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/banking': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/certification': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/marketing': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/operations': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/association': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/app-center': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/bank-dashboard': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/service-dashboard': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/dashboard': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
