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
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'

  // PROTECTED ROUTES: require authentication
  if (to.meta.requiresAuth) {
    // Guest users can access protected routes (limited functionality)
    if (isGuest) {
      return next()
    }
    
    // Check localStorage first (for cross-domain authentication)
    if (isAuthenticated) {
      return next()
    }

    // Fallback: verify authentication with backend (only if not in localStorage)
    try {
      // Make API call to check authentication status
      const res = await api.get('/auth/me/', { withCredentials: true })
      
      // If user is authenticated, store in localStorage and allow access
      if (res.data.is_authenticated === true) {
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('username', res.data.username)
        return next()
      }

      // Not authenticated: clear localStorage and redirect to login
      localStorage.removeItem('isAuthenticated')
      localStorage.removeItem('username')
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    } catch (error) {
      // API call failed: clear localStorage and redirect to login
      localStorage.removeItem('isAuthenticated')
      localStorage.removeItem('username')
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    }
  }

  // GUEST-ONLY ROUTES: login and register pages
  if (to.meta.guestOnly) {
    // If already authenticated via localStorage, redirect to dashboard
    if (isAuthenticated) {
      const redirect = to.query.redirect || '/dashboard'
      return next(redirect)
    }

    // If in guest mode, redirect to dashboard
    if (isGuest) {
      return next('/dashboard')
    }

    // Fallback: check with backend
    try {
      // Check if user is already authenticated
      const res = await api.get('/auth/me/', { withCredentials: true })

      // If authenticated, store in localStorage and redirect to dashboard
      if (res.data.is_authenticated === true) {
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('username', res.data.username)
        const redirect = to.query.redirect || '/dashboard'
        return next(redirect)
      }
    } catch (error) {
      // API error: allow access to login/register page
    }
  }

  // No restrictions: allow navigation
  next()
})

export default router