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
  const hasUsername = !!localStorage.getItem('username')

  // PROTECTED ROUTES: require authentication
  if (to.meta.requiresAuth) {
    // Guest users can access protected routes (limited functionality)
    if (isGuest) {
      return next()
    }

    // Quick check: if no username in localStorage, redirect immediately
    if (!hasUsername) {
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    }

    // Verify with backend API
    try {
      const res = await api.get('/auth/me/', { withCredentials: true })
      
      // If user is authenticated, allow access
      if (res.data.is_authenticated === true) {
        return next()
      }

      // Not authenticated: clear localStorage and redirect to login
      localStorage.removeItem('username')
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    } catch (error) {
      // API call failed: clear localStorage and redirect to login
      localStorage.removeItem('username')
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    }
  }

  // GUEST-ONLY ROUTES: login and register pages
  if (to.meta.guestOnly) {
    // If user has username in localStorage, they might be logged in
    if (hasUsername) {
      try {
        // Verify with backend
        const res = await api.get('/auth/me/', { withCredentials: true })

        // If authenticated, redirect to dashboard
        if (res.data.is_authenticated === true) {
          const redirect = to.query.redirect || '/dashboard'
          return next(redirect)
        }
      } catch (error) {
        // API error: clear stale data
        localStorage.removeItem('username')
      }
    }

    // If in guest mode, redirect to dashboard
    if (isGuest) {
      return next('/dashboard')
    }
  }

  // No restrictions: allow navigation
  next()
})

export default router