// vite.config.js
// Vite build tool configuration
// Handles development server, path aliases, and API proxy

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [
    vue(),  // Vue 3 support
    vueDevTools(),  // Vue DevTools browser extension support
  ],
  
  resolve: {
    alias: {
      // '@' maps to 'src' folder - allows imports like '@/components/Navbar.vue'
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  
  server: {
    host: '127.0.0.1',  // Localhost address
    port: 5173,  // Development server port (default Vite port)
    
    /**
     * Proxy Configuration
     * Forwards API requests from frontend (port 5173) to backend (port 8000)
     * - Prevents CORS issues during development
     * - Makes backend appear to be on same origin as frontend
     */
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',  // Django local backend URL 
        changeOrigin: false,  // Keep false to preserve cookies (important for auth)
        secure: false,  // Allow self-signed certificates (dev only)
        ws: true,  // Enable WebSocket proxying (if needed later)
        
        /**
         * Optional: Configure proxy events for debugging
         * Uncomment console.logs if you need to debug API calls
         */
        configure: (proxy, options) => {
          // Fires when request is sent to backend
          proxy.on('proxyReq', (proxyReq, req, res) => {
            // console.log('→ Proxying:', req.method, req.url)
          });
          
          // Fires when response is received from backend
          proxy.on('proxyRes', (proxyRes, req, res) => {
            // console.log('← Response:', proxyRes.statusCode, req.url)
          });
        }
      }
    }
  }
})