<!-- 
  Main Navigation Component
  - Responsive navbar with mobile sidebar
  - Handles authentication states (logged in, guest, not logged in)
  - Syncs with backend on mount to verify auth status
  - Supports hash-based navigation for same-page sections
-->
<template>
  <!-- Main navbar: fixed at top, changes style on scroll and based on route -->
  <nav class="navbar" :class="{ scrolled: isScrolled, transparent: isTransparent }">
    <div class="nav-container">
      
      <!-- Logo Section: links to home page -->
      <router-link to="/" class="logo-wrapper">
        <div class="logo-icon">
          <Calculator :size="24" />
        </div>
        <span class="logo-text">CalculatorPro</span>
      </router-link>

      <!-- Desktop Navigation Links: hidden on mobile -->
      <div class="nav-links">
        <!-- Dynamic nav links: loops through navLinks array -->
        <a
          v-for="link in navLinks"
          :key="link.path"
          @click.prevent="handleNavClick(link)"
          class="nav-link"
          :class="{ active: isActive(link.path) }"
          href="#"
        >
          <component :is="link.icon" :size="18" />
          <span>{{ link.label }}</span>
        </a>
        
        <!-- Account Button: shows for authenticated or guest users -->
        <a
          v-if="username || isGuest"
          @click.prevent="handleNavClick({ path: '/dashboard', isHash: false })"
          class="nav-link account-link"
          :class="{ active: $route.path === '/dashboard' }"
          href="#"
        >
          <User :size="18" />
          <span>Account</span>
          <!-- Animated arrow indicator -->
          <ChevronRight :size="16" class="account-arrow" />
        </a>
      </div>

      <!-- Right side actions: auth buttons or user info -->
      <div class="nav-actions">
        
        <!-- GUEST MODE BADGE: shows when user is in guest mode -->
        <template v-if="isGuest && !username">
          <div class="user-badge guest-badge">
            <Shield :size="16" />
            <span>Guest Mode</span>
          </div>
          <!-- Exit guest mode button -->
          <button class="logout-btn" @click="exitGuest" title="Exit Guest Mode">
            <LogOut :size="18" />
          </button>
        </template>

        <!-- LOGGED IN USER BADGE: shows username when authenticated -->
        <template v-else-if="username">
          <div class="user-badge user-badge-active">
            <User :size="16" />
            <span>{{ username }}</span>
          </div>
          <!-- Sign out button -->
          <button class="logout-btn" @click="logout" title="Sign Out">
            <LogOut :size="18" />
          </button>
        </template>

        <!-- AUTH BUTTONS: shows when not logged in or guest -->
        <div v-else class="auth-buttons">
          <router-link to="/login" class="btn btn-ghost">
            <LogIn :size="16" /> Sign in
          </router-link>
          <router-link to="/register" class="btn btn-primary">
            <Rocket :size="16" /> Get Started
          </router-link>
        </div>

        <!-- Mobile Menu Toggle: only visible on mobile -->
        <button class="mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
          <Menu v-if="!mobileMenuOpen" />
          <X v-else />
        </button>
      </div>
    </div>

    <!-- MOBILE SIDEBAR: teleported to body for proper z-index stacking -->
    <teleport to="body">
      <!-- Slide transition for smooth open/close -->
      <transition name="sidebar">
        <div v-if="mobileMenuOpen" class="mobile-sidebar">
          
          <!-- Sidebar header with logo and close button -->
     <div class="sidebar-header">
  <div class="sidebar-logo-wrapper">
    <div class="sidebar-logo-icon">
      <Calculator :size="20" /> 
    </div>
    <span class="sidebar-logo-text">CalculatorPro</span>
  </div>
            <button class="sidebar-close-btn" @click="mobileMenuOpen = false">
              <X />
            </button>
          </div>

          <!-- User info card: shows guest or authenticated user details -->
          <div
            v-if="username || isGuest"
            class="sidebar-user-info"
            :class="{ guest: isGuest }"
          >
            <div class="user-avatar-large">
              <Shield v-if="isGuest" :size="24" />
              <User v-else :size="24" />
            </div>
            <div class="user-details">
              <div class="user-name">{{ username || 'Guest Mode' }}</div>
              <div class="user-email">{{ isGuest ? 'Limited access' : 'Authenticated' }}</div>
            </div>
          </div>

          <!-- Sidebar navigation links -->
          <div class="sidebar-links">
            <a
              v-for="link in navLinks"
              :key="link.path"
              @click.prevent="handleNavClick(link)"
              class="sidebar-link"
              :class="{ active: isActive(link.path) }"
              href="#"
            >
              <component :is="link.icon" :size="18" />
              {{ link.label }}
            </a>
            
            <!-- Mobile account link with special styling -->
            <a
              v-if="username || isGuest"
              @click.prevent="handleNavClick({ path: '/dashboard', isHash: false })"
              class="sidebar-link account-link-mobile"
              :class="{ active: $route.path === '/dashboard' }"
              href="#"
            >
              <User :size="18" />
              Account
              <ChevronRight :size="18" class="account-arrow-mobile" />
            </a>
          </div>

          <!-- Sidebar footer with auth actions -->
          <div class="sidebar-actions">
            <!-- Logout for authenticated users -->
            <button v-if="username" class="sidebar-logout" @click="logout">
              <LogOut :size="18" />
              Sign Out
            </button>

            <!-- Exit guest mode button -->
            <button
              v-else-if="isGuest"
              class="sidebar-logout"
              @click="exitGuest"
            >
              <LogOut :size="18" />
              Exit Guest Mode
            </button>

            <!-- Auth buttons for non-authenticated users -->
            <div v-else class="sidebar-auth-buttons">
              <router-link to="/login" class="sidebar-btn ghost" @click="mobileMenuOpen = false">
                <LogIn :size="18" />
                Sign In
              </router-link>
              <router-link to="/register" class="sidebar-btn primary" @click="mobileMenuOpen = false">
                <Rocket :size="18" />
                Get Started
              </router-link>
            </div>
          </div>
        </div>
      </transition>

      <!-- Backdrop: darkens background when sidebar is open -->
      <div
        v-if="mobileMenuOpen"
        class="sidebar-backdrop"
        @click="mobileMenuOpen = false"
      />
    </teleport>
  </nav>
</template>

<script>
// Importing all required icons from lucide-vue-next
import {
  Calculator,
  Home,
  LayoutDashboard,
  User,
  Shield,
  ChevronDown,
  ChevronRight,
  Rocket,
  LogOut,
  LogIn,
  Menu,
  X,
  Zap,
  Star
} from 'lucide-vue-next'

import api from '@/services/api'

export default {
  name: 'NavbarComponent',

  components: {
    Calculator,
    Home,
    LayoutDashboard,
    User,
    Shield,
    ChevronDown,
    ChevronRight,
    Rocket,
    LogOut,
    LogIn,
    Menu,
    X,
    Zap,
    Star
  },

  data() {
    return {
      isScrolled: false,  // Tracks if user has scrolled down
      mobileMenuOpen: false,  // Controls mobile sidebar visibility
      userMenuOpen: false,  // Controls user dropdown menu (currently unused)

      // Load username from localStorage for instant display (prevents flicker)
      username: localStorage.getItem('username'),
      authChecked: false,  // Flag to know when backend sync is complete

      // Navigation links configuration
      navLinks: [
        { label: 'Home', path: '/', icon: 'Home' },
        { label: 'Features', path: '/#features', icon: 'Zap', isHash: true },  // isHash flag for scroll behavior
        { label: 'Access Modes', path: '/#access', icon: 'Star', isHash: true }
      ]
    }
  },

  computed: {
    // Check if user is authenticated
    isAuthenticated() {
      return !!this.username
    },

    // Check if user is in guest mode (not authenticated but has guest flag)
    isGuest() {
      return !this.isAuthenticated && localStorage.getItem('is_guest') === 'true'
    },

    // Transparent navbar only on homepage when not scrolled
    isTransparent() {
      return this.$route.path === '/' && !this.isScrolled
    }
  },

  mounted() {
    // Listen for scroll events to add shadow to navbar
    window.addEventListener('scroll', () => {
      this.isScrolled = window.scrollY > 20
    })

    // Sync authentication state with backend on component mount
    this.syncAuth()
  },

  methods: {
    // Verifies authentication with backend and updates local state
    async syncAuth() {
      try {
        const res = await api.get('/auth/me/', { withCredentials: true })

        if (res.data.is_authenticated) {
          // User is authenticated: update username
          this.username = res.data.username
          localStorage.setItem('username', res.data.username)
          localStorage.removeItem('is_guest')  // Clear guest flag if present
        } else {
          // Not authenticated: clear auth data
          this.clearAuth()
        }
      } catch {
        // API call failed: assume not authenticated
        this.clearAuth()
      } finally {
        this.authChecked = true  // Mark sync as complete
      }
    },

    // Clears authentication data from component and localStorage
    clearAuth() {
      this.username = null
      localStorage.removeItem('username')
    },

    // Closes all open menus
    closeMenus() {
      this.userMenuOpen = false
      this.mobileMenuOpen = false
    },

    // Handles user logout
    async logout() {
      try {
        // Call backend logout endpoint
        await api.post('/auth/logout/', {}, { withCredentials: true })
      } catch (e) {
        console.warn('Logout failed (safe to ignore)')
      }

      // Clear all auth data
      this.clearAuth()
      localStorage.removeItem('is_guest')
      this.closeMenus()
      
      // Redirect to login page
      this.$router.push('/login')
    },

    // Exits guest mode and redirects to login
    exitGuest() {
      localStorage.removeItem('is_guest')
      this.closeMenus()
      this.$router.push('/login')
    },

    // Checks if a nav link is currently active
    isActive(path) {
      if (path.startsWith('/#')) return false  // Hash links never show as active
      return this.$route.path === path
    },

    // Handles navigation link clicks (supports both routes and hash scrolls)
    handleNavClick(link) {
      if (link.isHash) {
        // Extract section ID from hash (e.g., '/#features' -> 'features')
        const sectionId = link.path.substring(2)

        // If not on homepage, navigate there first then scroll
        if (this.$route.path !== '/') {
          this.$router.push('/').then(() => {
            setTimeout(() => {
              document.getElementById(sectionId)?.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
              })
            }, 100)  // Small delay to ensure page is loaded
          })
        } else {
          // Already on homepage: just scroll to section
          document.getElementById(sectionId)?.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          })
        }
      } else {
        // Regular route navigation
        this.$router.push(link.path)
      }

      // Close mobile menu after navigation
      this.closeMenus()
    }
  }
}
</script>

<style scoped>
/* ============================================
   NAVBAR STYLES
   ============================================ */

/* Fixed navbar with glassmorphism effect */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999997;  /* High z-index to stay above content */
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(30px);  /* Creates frosted glass effect */
  -webkit-backdrop-filter: blur(30px);  /* Safari support */
  border-bottom: 1px solid rgba(0,0,0,0.08);
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
}

/* Transparent state on homepage before scroll */
.navbar.transparent {
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border-bottom: none;
}

/* Scrolled state adds shadow for depth */
.navbar.scrolled {
  background: rgba(255,255,255,0.98);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}

/* Main container with max-width for large screens */
.nav-container {
  max-width: 1480px;
  margin: 0 auto;
  padding: 1rem 5vw;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 70px;
  gap: 2rem;
}

/* ============================================
   LOGO SECTION
   ============================================ */

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  transition: all 0.3s ease;
  flex-shrink: 0;  /* Prevents logo from shrinking */
}

.logo-wrapper:hover {
  transform: translateY(-2px);  /* Subtle lift on hover */
}

.logo-icon {
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(59,130,246,0.2);
}

.logo-text {
  font-size: 1.4rem;
  font-weight: 800;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ============================================
   DESKTOP NAVIGATION LINKS
   ============================================ */

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;  /* Takes available space */
  justify-content: center;
  margin: 0 auto;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.2rem;
  color: #64748b;
  font-weight: 500;
  font-size: 0.95rem;
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.nav-link:hover {
  color: #1e293b;
  background: rgba(59,130,246,0.06);
}

.nav-link.active {
  color: #3b82f6;
  background: rgba(59,130,246,0.08);
  font-weight: 600;
}

/* Special styling for Account link - premium look */
.nav-link.account-link {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.1) 100%);
  color: #6366f1;
  font-weight: 600;
  border: 1.5px solid rgba(99, 102, 241, 0.3);
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.15),
              inset 0 1px 0 rgba(255, 255, 255, 0.5);
  margin-left: 0.5rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Shimmer effect on hover */
.nav-link.account-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.15), transparent);
  transition: left 0.6s ease;
}

.nav-link.account-link:hover::before {
  left: 100%;  /* Moves shimmer across */
}

.nav-link.account-link:hover {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(139, 92, 246, 0.15) 100%);
  border-color: rgba(99, 102, 241, 0.5);
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3),
              0 2px 8px rgba(139, 92, 246, 0.2),
              inset 0 1px 0 rgba(255, 255, 255, 0.6);
  color: #4f46e5;
}

.nav-link.account-link:active {
  transform: translateY(-1px) scale(1);
}

.nav-link.account-link.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.22) 0%, rgba(139, 92, 246, 0.18) 100%);
  border-color: rgba(99, 102, 241, 0.6);
  color: #4338ca;
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35),
              inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

/* Animated arrow - continuous movement */
.account-arrow {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin-left: 0.25rem;
  animation: arrowMoveContinuous 1.2s ease-in-out infinite;
}

@keyframes arrowMoveContinuous {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(6px); }
}

/* ============================================
   USER BADGES AND AUTH BUTTONS
   ============================================ */

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
  margin-left: auto;
}

/* User badge - shows username or guest status */
.user-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

/* Guest mode badge styling */
.guest-badge {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.1));
  border: 1px dashed #f59e0b;
  color: #92400e;
}

.guest-badge svg {
  color: #d97706;
}

/* Authenticated user badge styling */
.user-badge-active {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(37, 99, 235, 0.08));
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: #1e40af;
}

.user-badge-active svg {
  color: #3b82f6;
}

/* Logout button */
.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.3);
  transform: translateY(-2px);
}

.logout-btn:active {
  transform: translateY(0);
}

/* Auth buttons container */
.auth-buttons {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Base button styles */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.25rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  transition: all 0.3s ease;
}

/* Ghost button (outlined) */
.btn-ghost {
  background: transparent;
  border: 1.5px solid rgba(0,0,0,0.15);
  color: #1e293b;
}

.btn-ghost:hover {
  background: rgba(0,0,0,0.04);
  border-color: rgba(0,0,0,0.25);
}

/* Primary button (filled with gradient) */
.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(59,130,246,0.25);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(59,130,246,0.35);
}

/* ============================================
   MOBILE MENU BUTTON
   ============================================ */

.mobile-menu-btn {
  background: none;
  border: none;
  color: #1e293b;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: background 0.2s;
  display: none;  /* Hidden by default, shown on mobile */
}

.mobile-menu-btn:hover {
  background: rgba(0,0,0,0.05);
}

/* ============================================
   MOBILE SIDEBAR
   ============================================ */

.mobile-sidebar {
  position: fixed !important;
  top: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 320px;
  max-width: 85vw;
  background: white !important;
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.15) !important;
  z-index: 2147483647 !important;  /* Maximum z-index */
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

/* Sidebar header */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.03), rgba(139, 92, 246, 0.03));
}

/* Close button in sidebar */
.sidebar-close-btn {
  background: rgba(0, 0, 0, 0.05);
  border: none;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.sidebar-close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #1e293b;
}

/* User info card in sidebar */
.sidebar-user-info {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1.25rem;
  margin: 1rem 1.25rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.08));
  border-radius: 14px;
  border: 1px solid rgba(59, 130, 246, 0.12);
}

/* Guest variant of user info */
.sidebar-user-info.guest {
  border: 1px solid rgba(245, 158, 11, 0.4);
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.1));
}

/* User avatar in sidebar */
.user-avatar-large {
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

/* User details text */
.user-details {
  flex: 1;
  min-width: 0;  /* Allows text truncation */
}

.user-details .user-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-details .user-email {
  color: #64748b;
  font-size: 0.85rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Sidebar links container */
.sidebar-links {
  flex: 1;
  padding: 0.5rem 1.25rem 1.5rem;
}

/* Individual sidebar link */
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem 1rem;
  margin-bottom: 0.25rem;
  font-size: 0.975rem;
  font-weight: 500;
  color: #475569;
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.2s;
  cursor: pointer;
}

.sidebar-link:hover {
  background: rgba(59, 130, 246, 0.08);
  color: #1e293b;
}

.sidebar-link.active {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(139, 92, 246, 0.08));
  color: #3b82f6;
  font-weight: 600;
}

/* Mobile account link - premium styling */
.sidebar-link.account-link-mobile {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.12) 100%);
  color: #6366f1;
  font-weight: 700;
  border: 2px solid rgba(99, 102, 241, 0.35);
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2),
              inset 0 1px 0 rgba(255, 255, 255, 0.5);
  margin-top: 0.75rem;
  padding: 1rem 1.2rem;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Shimmer effect for mobile account link */
.sidebar-link.account-link-mobile::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.2), transparent);
  transition: left 0.6s ease;
}

.sidebar-link.account-link-mobile:hover::before {
  left: 100%;
}

.sidebar-link.account-link-mobile:hover {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.22) 0%, rgba(139, 92, 246, 0.18) 100%);
  border-color: rgba(99, 102, 241, 0.55);
  transform: translateX(6px) scale(1.02);
  box-shadow: 0 6px 24px rgba(99, 102, 241, 0.35),
              0 3px 10px rgba(139, 92, 246, 0.25),
              inset 0 1px 0 rgba(255, 255, 255, 0.6);
  color: #4f46e5;
}

.sidebar-link.account-link-mobile:active {
  transform: translateX(3px) scale(1);
}

.sidebar-link.account-link-mobile.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.28) 0%, rgba(139, 92, 246, 0.22) 100%);
  border-color: rgba(99, 102, 241, 0.65);
  color: #4338ca;
  box-shadow: 0 5px 20px rgba(99, 102, 241, 0.4),
              inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

/* Animated arrow in mobile account link */
.account-arrow-mobile {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin-left: auto;
  animation: arrowMoveContinuous 1.2s ease-in-out infinite;
}

/* Sidebar actions footer */
.sidebar-actions {
  margin-top: auto;  /* Pushes to bottom */
  padding: 1.25rem;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
}

/* Logout button in sidebar */
.sidebar-logout {
  width: 100%;
  padding: 0.8rem;
  border-radius: 10px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  font-weight: 700;
  color: #ef4444;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  transition: all 0.2s;
}

.sidebar-logout:hover {
  background: rgba(239, 68, 68, 0.15);
}

/* Auth buttons container in sidebar */
.sidebar-auth-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Sidebar button base styles */
.sidebar-btn {
  padding: 0.875rem 1rem;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.975rem;
  text-align: center;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  transition: all 0.2s;
}

/* Ghost variant in sidebar */
.sidebar-btn.ghost {
  background: transparent;
  border: 2px solid #3b82f6;
  color: #3b82f6;
}

.sidebar-btn.ghost:hover {
  background: rgba(59, 130, 246, 0.08);
}

/* Primary variant in sidebar */
.sidebar-btn.primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.sidebar-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(59, 130, 246, 0.4);
}

/* Sidebar backdrop - darkens background */
.sidebar-backdrop {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(0, 0, 0, 0.5) !important;
  z-index: 2147483646 !important;  /* Just below sidebar */
  backdrop-filter: blur(4px);  /* Blur effect */
}

/* ============================================
   TRANSITION ANIMATIONS
   ============================================ */

/* Slide-in animation for sidebar */
.sidebar-enter-active,
.sidebar-leave-active {
  transition: transform 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.sidebar-enter-from,
.sidebar-leave-to {
  transform: translateX(100%);  /* Slides in from right */
}

/* ============================================
   RESPONSIVE BREAKPOINTS
   ============================================ */

/* Tablet and mobile: hide desktop nav, show mobile menu */
@media (max-width: 1024px) {
  .nav-links,
  .auth-buttons,
  .user-badge,
  .logout-btn {
    display: none;
  }
 
  .mobile-menu-btn {
    display: block;
  }
}

/* Small mobile adjustments */
@media (max-width: 380px) {
  .mobile-sidebar {
    width: 280px;
  }
 
  .sidebar-header {
    padding: 1.25rem 1rem;
  }
 
  .sidebar-user-info {
    margin: 0.875rem 1rem;
    padding: 1rem;
  }
 
  .user-avatar-large {
    width: 46px;
    height: 46px;
  }
 
  .sidebar-links {
    padding: 0.5rem 1rem;
  }
 
  .sidebar-actions {
    padding: 1rem;
  }
}
.sidebar-logo-wrapper {
  display: flex;
  align-items: center;
  gap: 0.65rem;  /* Icon aur text ke beech space */
}

.sidebar-logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 3px 10px rgba(59,130,246,0.2);
  flex-shrink: 0;
}

.sidebar-logo-text {
  font-size: 1.25rem;
  font-weight: 800;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;  /* Gradient text effect */
}
</style>