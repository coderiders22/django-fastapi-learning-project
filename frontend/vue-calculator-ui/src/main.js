// Import Vue and necessary dependencies
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/gradient.css'

// Import Navbar globally so it's available everywhere
import Navbar from '@/components/Navbar.vue'
import { initCSRF } from '@/services/api'

/**
 * Bootstrap function to initialize the app
 * This ensures CSRF token is fetched before the app starts
 */
async function bootstrap() {
  try {
    // Initialize CSRF token for secure API requests
    await initCSRF()
  } catch (e) {
    // If CSRF fails, just log a warning and continue
    // The app can still work, but API calls might fail
    console.warn('CSRF init error:', e)
  }

  // Create Vue app instance
  const app = createApp(App)
  
  // Register router for navigation between pages
  app.use(router)
  
  // Register Navbar globally so we don't need to import it in every component
  app.component('Navbar', Navbar)
  
  // Mount the app to the DOM element with id="app"
  app.mount('#app')
}

// Start the application
bootstrap()