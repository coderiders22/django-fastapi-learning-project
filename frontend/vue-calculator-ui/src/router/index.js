// router/index.js
// Vue Router configuration with authentication guards
// Handles protected routes, guest-only routes, and 404 fallback

import { createRouter, createWebHistory } from 'vue-router'
import api from '@/services/api'

// Import all view components
import Welcome from '../views/Welcome.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import NotFound from '../views/NotFound.vue'

// Route definitions with metadata for guards
const routes = [
  { 
    path: '/', 
    name: 'Welcome', 
    component: Welcome 
  },
  { 
    path: '/login', 
    name: 'Login', 
    component: Login, 
    meta: { guestOnly: true }  // Only accessible when not logged in
  },
  { 
    path: '/register', 
    name: 'Register', 
    component: Register, 
    meta: { guestOnly: true }  // Only accessible when not logged in
  },
  { 
    path: '/dashboard', 
    name: 'Dashboard', 
    component: Dashboard, 
    meta: { requiresAuth: true }  // Requires authentication
  },
  { 
    path: '/:pathMatch(.*)*',  // Catch-all route for 404
    name: 'NotFound', 
    component: NotFound 
  }
]

// Create router instance with HTML5 history mode
const router = createRouter({
  history: createWebHistory(),  // Uses browser's History API (no # in URLs)
  routes
})

// Navigation Guard: runs before every route change
router.beforeEach(async (to, from, next) => {
  // Check if user is in guest mode (stored in localStorage)
  const isGuest = localStorage.getItem('is_guest') === 'true'

  // PROTECTED ROUTES: require authentication
  if (to.meta.requiresAuth && isGuest) {
    // Guest users can access protected routes (limited functionality)
    return next()
  }

  // For non-guest users, verify authentication
  if (to.meta.requiresAuth) {
    // Check if user is authenticated via localStorage flag
    // This avoids API call on every navigation which might fail due to network/CORS issues
    const isAuthenticated = localStorage.getItem('is_authenticated') === 'true'

    if (isAuthenticated) {
      return next()
    }

    // Not authenticated: redirect to login
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  // GUEST-ONLY ROUTES: login and register pages
  if (to.meta.guestOnly) {
    const isAuthenticated = localStorage.getItem('is_authenticated') === 'true'

    // If authenticated, redirect to dashboard
    if (isAuthenticated) {
      return next('/dashboard')
    }
  }

  // No restrictions: allow navigation
  next()
})

export default router