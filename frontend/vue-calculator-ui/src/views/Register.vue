<!-- src/views/Register.vue -->
<template>
  <div class="auth-page">
    <Navbar />

    <div class="auth-wrapper">
      <!-- ================= LEFT SIDE - BRANDING ================= -->
      <!-- Marketing content explaining benefits of registration -->
      <div class="auth-branding">
        <div class="branding-content">
          <!-- Badge showing this is registration page -->
          <div class="brand-badge">
            <UserPlus :size="16" />
            <span>New Account</span>
          </div>

          <h2 class="branding-title">
            Join CalculatorPro<span class="gradient-text">today</span>
          </h2>

          <p class="branding-description">
            Create your free account and unlock premium features including unlimited 
            calculations, smart notes, and complete history management.
          </p>

          <!-- List of features user gets after registration -->
          <div class="feature-list">
            <div class="feature-item">
              <div class="feature-icon">
                <Zap :size="18" />
              </div>
              <div class="feature-text">
                <strong>Instant Premium Access</strong>
                <span>Automatically logged in with full features enabled</span>
              </div>
            </div>

            <div class="feature-item">
              <div class="feature-icon">
                <FileText :size="18" />
              </div>
              <div class="feature-text">
                <strong>Unlimited Notes</strong>
                <span>Add context and reminders to all your calculations</span>
              </div>
            </div>

            <div class="feature-item">
              <div class="feature-icon">
                <TrendingUp :size="18" />
              </div>
              <div class="feature-text">
                <strong>Weekly Analytics</strong>
                <span>Track your productivity with detailed statistics</span>
              </div>
            </div>

            <div class="feature-item">
              <div class="feature-icon">
                <Database :size="18" />
              </div>
              <div class="feature-text">
                <strong>Cloud Storage</strong>
                <span>Your data is securely saved and synced across devices</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ================= RIGHT SIDE - REGISTRATION FORM ================= -->
      <div class="auth-form-section">
        <div class="auth-container">
          <div class="auth-card">
            <!-- Card header with icon and title -->
            <div class="card-header">
              <div class="header-icon">
                <UserPlus :size="28" />
              </div>
              <h1>Create your account</h1>
              <p class="header-subtitle">
                Start with premium access — no credit card required
              </p>
            </div>

            <!-- Registration form with validation -->
            <form @submit.prevent="register" class="auth-form">
              <!-- Username input field -->
              <div class="form-group">
                <label for="username">
                  <User :size="16" />
                  <span>Username</span>
                </label>
                <div class="input-wrapper">
                  <input
                    id="username"
                    v-model="username"
                    type="text"
                    placeholder="Choose a unique username"
                    autocomplete="username"
                    required
                    :class="{ 'input-error': errors.username }"
                  />
                </div>
                <!-- Show username error if exists -->
                <span v-if="errors.username" class="error-text">
                  <AlertCircle :size="14" />
                  {{ errors.username }}
                </span>
              </div>

              <!-- Password input field with toggle visibility -->
              <div class="form-group">
                <label for="password">
                  <Lock :size="16" />
                  <span>Password</span>
                </label>
                <div class="input-wrapper password-wrapper">
                  <input
                    id="password"
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Create a strong password"
                    autocomplete="new-password"
                    required
                    :class="{ 'input-error': errors.password }"
                  />
                  <!-- Toggle button to show/hide password -->
                  <button
                    type="button"
                    class="toggle-password"
                    @click="showPassword = !showPassword"
                    tabindex="-1"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'"
                  >
                    <Eye v-if="showPassword" :size="18" />
                    <EyeOff v-else :size="18" />
                  </button>
                </div>
                <!-- Show password error if exists -->
                <span v-if="errors.password" class="error-text">
                  <AlertCircle :size="14" />
                  {{ errors.password }}
                </span>
              </div>

              <!-- Password Strength Indicator -->
              <!-- Only shows when user starts typing password -->
              <div class="password-strength" v-if="password">
                <div class="strength-label">
                  <span>Password strength</span>
                  <!-- Dynamic strength text (Weak/Fair/Good/Strong) -->
                  <span class="strength-text" :class="passwordStrengthClass">
                    {{ passwordStrengthText }}
                  </span>
                </div>
                <!-- Visual strength bar that fills based on password quality -->
                <div class="strength-bar">
                  <div
                    class="strength-fill"
                    :class="passwordStrengthClass"
                    :style="{ width: passwordStrengthWidth }"
                  ></div>
                </div>
              </div>

              <!-- Submit button with loading state -->
              <button
                type="submit"
                class="submit-btn"
                :disabled="loading"
                :class="{ 'loading': loading }"
              >
                <!-- Show spinner when submitting -->
                <span v-if="loading" class="btn-content">
                  <span class="spinner"></span>
                  <span>Creating account...</span>
                </span>
                <!-- Normal state -->
                <span v-else class="btn-content">
                  <span>Create Premium Account</span>
                  <ArrowRight :size="18" />
                </span>
              </button>
            </form>

            <!-- Guest Mode Option -->
            <!-- Allows users to skip registration and try as guest -->
            <div class="guest-hint">
              <p>
                Just want to try? 
                <button class="guest-link" @click="continueAsGuest">
                  Continue as Guest
                </button>
              </p>
            </div>

            <div class="divider">
              <span>or</span>
            </div>

            <!-- Link to login page for existing users -->
            <div class="footer-links">
              <p>
                Already have an account?
                <router-link to="/login" class="login-link">
                  Sign in here
                  <ArrowRight :size="14" />
                </router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Message Modal for success/error notifications -->
    <Modal
      v-if="showMessage"
      :text="message"
      :type="messageType"
      @close="showMessage = false"
    />

    <!-- Full-screen Loading Overlay during registration -->
    <div v-if="isFullLoading" class="full-loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p class="loading-text">Creating your premium account...</p>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script>
// Import all necessary icons
import {
  Eye,
  EyeOff,
  UserPlus,
  User,
  Lock,
  ArrowRight,
  Zap,
  Shield,
  AlertCircle,
  FileText,
  TrendingUp,
  Database
} from 'lucide-vue-next'

import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import api from '@/services/api'
import Modal from '@/components/Modal.vue'

export default {
  name: 'Register',

  components: {
    Navbar,
    Footer,
    Modal,
    Eye,
    EyeOff,
    UserPlus,
    User,
    Lock,
    ArrowRight,
    Zap,
    Shield,
    AlertCircle,
    FileText,
    TrendingUp,
    Database
  },

  data() {
    return {
      username: '',              // User's chosen username
      password: '',              // User's chosen password
      showPassword: false,       // Toggle for password visibility
      loading: false,            // Button loading state
      isFullLoading: false,      // Full-screen loading overlay
      showMessage: false,        // Show/hide modal
      message: '',               // Modal message text
      messageType: 'error',      // Modal type (success/error)
      errors: {}                 // Form validation errors from backend
    }
  },

  computed: {
    // Calculate password strength based on multiple criteria
    passwordStrength() {
      if (!this.password) return 0

      let strength = 0
      // Check length (8+ chars = 1 point, 12+ chars = 2 points)
      if (this.password.length >= 8) strength++
      if (this.password.length >= 12) strength++
      // Check for lowercase letters
      if (/[a-z]/.test(this.password)) strength++
      // Check for uppercase letters
      if (/[A-Z]/.test(this.password)) strength++
      // Check for numbers
      if (/[0-9]/.test(this.password)) strength++
      // Check for special characters
      if (/[^a-zA-Z0-9]/.test(this.password)) strength++

      // Cap at 4 (Strong)
      return Math.min(strength, 4)
    },

    // CSS class for strength indicator color
    passwordStrengthClass() {
      const classes = ['weak', 'fair', 'good', 'strong']
      return classes[this.passwordStrength - 1] || 'weak'
    },

    // Text label for strength
    passwordStrengthText() {
      const texts = ['Weak', 'Fair', 'Good', 'Strong']
      return texts[this.passwordStrength - 1] || 'Weak'
    },

    // Width percentage for strength bar
    passwordStrengthWidth() {
      return `${(this.passwordStrength / 4) * 100}%`
    }
  },

  methods: {
    // Handle user registration
    async register() {
      // Clear previous errors
      this.errors = {}
      this.loading = true
      this.isFullLoading = true

      try {
        // Step 1: Register new user with Django backend
        const registerResponse = await api.post(
          '/auth/register/',
          {
            username: this.username,
            password: this.password
          },
          {
            withCredentials: true  // Include cookies for session
          }
        )

        // Backend auto-logs in the user after registration, 
        // so we don't need a separate login call
        // Verify the registration response
        if (!registerResponse.data || !registerResponse.data.username) {
          throw new Error('Registration verification failed')
        }

        // Store user authentication in localStorage for cross-domain compatibility
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('username', registerResponse.data.username)
        
        // Remove guest flag since user now has an account
        localStorage.removeItem('is_guest')

        // Show success message
        this.message =
          'Premium account created successfully! Redirecting to dashboard...'
        this.messageType = 'success'
        this.showMessage = true

        // Redirect to dashboard after a longer delay to ensure session is ready
        // Use window.location for a full page reload to ensure router guard
        // picks up the new authentication state
        setTimeout(() => {
          window.location.href = '/dashboard'
        }, 1200)

      } catch (err) {
  const data = err.response?.data

  // Password validation errors (list from Django)
  if (data?.password) {
    this.errors.password = data.password.join(' ')
  }

  // Username errors
  else if (data?.username) {
    this.errors.username = data.username[0]
  }

  // Generic backend error
  else if (data?.error) {
    this.message = data.error
    this.messageType = 'error'
    this.showMessage = true
  }

  else {
    this.message = 'Something went wrong. Please try again.'
    this.messageType = 'error'
    this.showMessage = true
  }


        this.messageType = 'error'
        this.showMessage = true
      } finally {
        // Reset loading states
        this.loading = false
        this.isFullLoading = false
      }
    },

    // Allow user to skip registration and use guest mode
    continueAsGuest() {
      localStorage.setItem('is_guest', 'true')
      this.$router.replace('/dashboard')
    }
  }
}
</script>


<style scoped>
/* ================= GLOBAL STYLES ================= */
.auth-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
  position: relative;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

/* Two-column layout for auth page */
.auth-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: calc(100vh - 70px);
  flex: 1;
}

/* ================= LEFT SIDE - BRANDING ================= */
.auth-branding {
  background: #f8f9fa;
  padding: 80px 5vw;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  margin: 0;
}

.branding-content {
  max-width: 520px;
  position: relative;
  z-index: 1;
  padding: 0 60px;
  margin: 0 auto;
}

/* Badge at top of branding section */
.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--primary);
  border-radius: 6px;
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.branding-title {
  font-size: 3rem;
  font-weight: 900;
  color: #1e293b;
  line-height: 1.2;
  margin-bottom: 0.75rem;
  letter-spacing: -0.02em;
}

.gradient-text {
  display: block;
  color: #1e293b;
}

.branding-description {
  font-size: 1.15rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 3rem;
}

/* Feature list on left side */
.feature-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

/* Icon containers for features */
.feature-icon {
  width: 40px;
  height: 40px;
  background: #1e293b;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.feature-text {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  color: #1e293b;
}

.feature-text strong {
  font-size: 1.05rem;
  font-weight: 600;
}

.feature-text span {
  font-size: 0.95rem;
  color: #64748b;
}

/* ================= RIGHT SIDE - FORM ================= */
.auth-form-section {
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 60px;
}

.auth-container {
  width: 100%;
  max-width: 480px;
}

/* Main registration card */
.auth-card {
  background: white;
  border-radius: 24px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 3rem 2.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.card-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

/* Icon at top of form */
.header-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 1.5rem;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.25);
}

.card-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  letter-spacing: -0.01em;
}

.header-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
}

/* ================= FORM STYLES ================= */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

/* Form labels with icons */
label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
}

label svg {
  color: var(--text-muted);
}

.input-wrapper {
  position: relative;
}

/* Input field styling */
input {
  width: 100%;
  padding: 1rem 1.25rem;
  background: #f8fafc;
  border: 2px solid transparent;
  border-radius: 12px;
  font-size: 1rem;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

/* Input focus state */
input:focus {
  outline: none;
  background: white;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

input::placeholder {
  color: var(--text-muted);
}

/* Error state for inputs */
.input-error {
  border-color: var(--danger) !important;
  background: rgba(239, 68, 68, 0.02) !important;
}

/* Error message text */
.error-text {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: var(--danger);
  font-size: 0.85rem;
  font-weight: 500;
}

/* Password field with toggle button */
.password-wrapper {
  position: relative;
}

/* Show/hide password toggle button */
.toggle-password {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.5rem;
  line-height: 1;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.toggle-password:hover {
  background: rgba(0, 0, 0, 0.04);
  color: var(--text-primary);
}

/* ================= PASSWORD STRENGTH INDICATOR ================= */
.password-strength {
  margin-top: -0.5rem;
}

.strength-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
}

.strength-label span:first-child {
  color: var(--text-secondary);
  font-weight: 500;
}

/* Strength text with dynamic colors */
.strength-text {
  font-weight: 600;
}

.strength-text.weak { color: #ef4444; }
.strength-text.fair { color: #f59e0b; }
.strength-text.good { color: #3b82f6; }
.strength-text.strong { color: #10b981; }

/* Strength bar container */
.strength-bar {
  height: 6px;
  background: rgba(0, 0, 0, 0.06);
  border-radius: 10px;
  overflow: hidden;
}

/* Strength bar fill (dynamically sized and colored) */
.strength-fill {
  height: 100%;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.strength-fill.weak { background: #ef4444; }
.strength-fill.fair { background: #f59e0b; }
.strength-fill.good { background: #3b82f6; }
.strength-fill.strong { background: #10b981; }

/* ================= SUBMIT BUTTON ================= */
.submit-btn {
  width: 100%;
  padding: 1.15rem;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  margin-top: 0.5rem;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
}

/* Loading spinner for submit button */
.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ================= GUEST HINT ================= */
.guest-hint {
  text-align: center;
  margin: 1.5rem 0;
  font-size: 0.95rem;
  color: var(--text-secondary);
}

.guest-hint p {
  margin: 0;
}

/* Guest mode link button */
.guest-link {
  background: none;
  border: none;
  color: var(--primary);
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
}

.guest-link:hover {
  color: var(--primary-dark);
}

/* Divider between form sections */
.divider {
  position: relative;
  text-align: center;
  margin: 2rem 0 1.5rem;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(0, 0, 0, 0.1);
}

.divider span {
  position: relative;
  background: white;
  padding: 0 1rem;
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 500;
}

/* ================= FOOTER LINKS ================= */
.footer-links {
  text-align: center;
}

.footer-links p {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

/* Login link styling */
.login-link {
  color: var(--primary);
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.login-link:hover {
  color: var(--primary-dark);
  gap: 0.5rem;
}

/* ================= FULL SCREEN LOADING OVERLAY ================= */
/* Shown during account creation process */
.full-loading-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.92);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 4000;
}

.loading-content {
  text-align: center;
  color: white;
}

/* Large spinner for full-screen loading */
.loading-spinner {
  width: 64px;
  height: 64px;
  border: 6px solid rgba(255, 255, 255, 0.2);
  border-top: 6px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

.loading-text {
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* ================= RESPONSIVE DESIGN ================= */
/* Tablet and smaller */
@media (max-width: 1024px) {
  /* Stack to single column */
  .auth-wrapper {
    grid-template-columns: 1fr;
  }
  
  /* Hide branding section on smaller screens */
  .auth-branding {
    display: none;
  }
  
  .auth-form-section {
    padding: 60px 30px;
  }
}

/* Mobile devices */
@media (max-width: 480px) {
  .auth-form-section {
    padding: 40px 20px;
  }
  
  .auth-card {
    padding: 2rem 1.5rem;
  }
  
  .card-header h1 {
    font-size: 1.5rem;
  }
  
  .header-icon {
    width: 50px;
    height: 50px;
  }
}
</style>