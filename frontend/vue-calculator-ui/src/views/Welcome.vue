<!-- src/views/Welcome.vue -->
<template>
  <div class="welcome-page">
    <!-- Loading Screen - Centered Spinner with Logo Inside + One-liner -->
    <transition name="fade">
      <div v-if="!authChecked" class="loading-overlay">
        <div class="loading-content">
          <div class="loader-wrapper">
            <div class="loader-ring">
              <Calculator class="loader-icon-inside" />
            </div>
          </div>
          <p class="loading-message">Unlocking smart calculations for you...</p>
        </div>
      </div>
    </transition>

    <!-- Main Content -->
    <div v-show="authChecked">
      <Navbar />

      <!-- ================= HERO SECTION ================= -->
      <section class="hero-section">
        <div class="hero-container">
          <div class="hero-content">
            <div class="badge-wrapper">
              <div class="badge">
                <Sparkles :size="16" class="badge-icon" />
                <span>Django • Vue.js • STGI Assessment • Full-Stack Calculator • 2026</span>
              </div>
            </div>

            <h1 class="hero-title">
              <span class="title-line">Professional. Powerful. Precise.</span>
              <span class="title-gradient">
                CalculatorPro<span class="dot">.</span>
              </span>
            </h1>

            <p class="hero-description">
              A feature-rich Django calculator with smart notes, weekly analytics,
              dual access modes, and intelligent history management. Experience the
              difference between guest and premium access.
            </p>

            <div class="hero-actions">
              <template v-if="isAuthenticated">
                <button class="btn btn-primary" @click="goDashboard">
                  <span>Go to Dashboard</span>
                  <ArrowRight :size="20" />
                </button>
              </template>

              <template v-else-if="isGuest">
                <button class="btn btn-primary" @click="goDashboard">
                  <span>Resume as Guest</span>
                  <ArrowRight :size="20" />
                </button>
                <button class="btn btn-secondary" @click="upgradeFromGuest">
                  <span>Register to Save History</span>
                </button>
              </template>

              <template v-else>
                <button class="btn btn-primary" @click="continueAsGuest">
                  <span>Continue as Guest</span>
                  <ArrowRight :size="20" />
                </button>
                <button class="btn btn-secondary" @click="goRegister">
                  <span>Login for Premium</span>
                </button>
              </template>
            </div>

            <div class="trust-indicators">
              <div class="trust-item">
                <CheckCircle2 :size="16" />
                <span>Guest & Premium Modes</span>
              </div>
              <div class="trust-item">
                <CheckCircle2 :size="16" />
                <span>Smart Notes System</span>
              </div>
              <div class="trust-item">
                <CheckCircle2 :size="16" />
                <span>Weekly Analytics</span>
              </div>
            </div>
          </div>

          <div class="hero-visual">
            <div class="visual-card">
              <div class="card-header">
                <div class="card-dots">
                  <span></span><span></span><span></span>
                </div>
                <div class="card-title">Live Calculation</div>
              </div>
              <div class="card-content">
                <div class="calc-display">
                  <div class="calc-operation">125 × 4</div>
                  <div class="calc-result">500</div>
                  <div class="calc-note">
                    <FileText :size="14" style="display: inline; margin-right: 6px;" />
                    Monthly revenue calculation
                  </div>
                </div>
                <div class="calc-history">
                  <div class="history-item">
                    <span>10 + 5</span>
                    <span>15</span>
                  </div>
                  <div class="history-item">
                    <span>20 ÷ 4</span>
                    <span>5</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="float-card float-1">
              <TrendingUp :size="16" />
              <span>Weekly Stats</span>
            </div>
            <div class="float-card float-2">
              <FileText :size="16" />
              <span>Smart Notes</span>
            </div>
            <div class="float-card float-3">
              <Shield :size="16" />
              <span>Secure Sessions</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= ACCESS COMPARISON SECTION ================= -->
      <section class="comparison-section" id="access">
        <div class="section-container">
          <div class="section-header">
            <div class="section-badge">Access Modes</div>
            <h2 class="section-title">Guest vs Premium Access</h2>
            <p class="section-description">
              Start free as a guest or unlock unlimited power with premium access.
            </p>
          </div>

          <div class="comparison-grid">
            <div class="access-card guest-card">
              <div class="access-header">
                <div class="access-icon guest-icon">
                  <User :size="28" />
                </div>
                <h3 class="access-title">Guest Mode</h3>
                <p class="access-subtitle">Try without registration</p>
              </div>
              <div class="access-features">
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>Basic calculator operations</span>
                </div>
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>View last 10 calculations</span>
                </div>
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>Add notes to 2 calculations</span>
                </div>
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>Weekly analytics dashboard</span>
                </div>
                <div class="feature-item disabled">
                  <XCircle :size="18" />
                  <span>Cannot clear full history</span>
                </div>
                <div class="feature-item disabled">
                  <XCircle :size="18" />
                  <span>Cannot delete individual items</span>
                </div>
                <div class="feature-item disabled">
                  <XCircle :size="18" />
                  <span>Session data not permanent</span>
                </div>
              </div>
              <button class="btn-access" @click="continueAsGuest">
                Try as Guest
              </button>
            </div>

            <div class="access-card premium-card">
              <div class="premium-badge">Recommended</div>
              <div class="access-header">
                <div class="access-icon premium-icon">
                  <Crown :size="28" />
                </div>
                <h3 class="access-title">Premium Access</h3>
                <p class="access-subtitle">Full power unleashed</p>
              </div>
              <div class="access-features">
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>Unlimited calculations</span>
                </div>
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>Complete calculation history</span>
                </div>
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>Unlimited notes on all calculations</span>
                </div>
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>Weekly calculation analytics</span>
                </div>
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>Delete individual history items</span>
                </div>
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>Clear entire history anytime</span>
                </div>
                <div class="feature-item enabled">
                  <CheckCircle2 :size="18" />
                  <span>Secure & persistent cloud storage</span>
                </div>
              </div>
              <button class="btn-access premium-btn" @click="goRegister">
                Get Premium Free
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= FEATURES SECTION ================= -->
      <section class="features-section" id="features">
        <div class="section-container">
          <div class="section-header">
            <div class="section-badge">Features</div>
            <h2 class="section-title">
              Everything you need for<br />professional calculations
            </h2>
            <p class="section-description">
              Built with Django REST Framework & Vue.js for maximum performance.
            </p>
          </div>

          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon" style="background:linear-gradient(135deg,#3b82f6,#2563eb)">
                <Calculator :size="24" />
              </div>
              <h3 class="feature-title">Advanced Calculator</h3>
              <p class="feature-description">
                Four basic operations with real-time validation, error handling, and instant results. Premium users get unlimited calculations.
              </p>
            </div>

            <div class="feature-card">
              <div class="feature-icon" style="background:linear-gradient(135deg,#8b5cf6,#7c3aed)">
                <History :size="24" />
              </div>
              <h3 class="feature-title">Smart History Tracking</h3>
              <p class="feature-description">
                Every calculation stored with full details, timestamps, and notes. Guest mode: 10 items. Premium: unlimited with full control.
              </p>
            </div>

            <div class="feature-card">
              <div class="feature-icon" style="background:linear-gradient(135deg,#10b981,#059669)">
                <FileText :size="24" />
              </div>
              <h3 class="feature-title">Calculation Notes</h3>
              <p class="feature-description">
                Add context to your calculations with smart notes. Guest users can add notes to 2 calculations. Premium users: unlimited notes.
              </p>
            </div>

            <div class="feature-card">
              <div class="feature-icon" style="background:linear-gradient(135deg,#f59e0b,#d97706)">
                <TrendingUp :size="24" />
              </div>
              <h3 class="feature-title">Weekly Analytics</h3>
              <p class="feature-description">
                Track your calculation patterns with weekly statistics. Available for both guest and premium users to monitor productivity.
              </p>
            </div>

            <div class="feature-card">
              <div class="feature-icon" style="background:linear-gradient(135deg,#ec4899,#db2777)">
                <Trash2 :size="24" />
              </div>
              <h3 class="feature-title">History Management</h3>
              <p class="feature-description">
                Premium users can delete individual history items or clear entire history. Guest users have read-only access to their 10 recent items.
              </p>
            </div>

            <div class="feature-card">
              <div class="feature-icon" style="background:linear-gradient(135deg,#06b6d4,#0891b2)">
                <Shield :size="24" />
              </div>
              <h3 class="feature-title">Secure Authentication</h3>
              <p class="feature-description">
                Django-powered authentication with session management. Guest sessions for quick access. User accounts for permanent data storage.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= STATS SECTION ================= -->
      <section class="stats-section">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-number">4</div>
            <div class="stat-label">Math Operations</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">2</div>
            <div class="stat-label">Access Modes</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">∞</div>
            <div class="stat-label">Premium Calculations</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">REST</div>
            <div class="stat-label">API Architecture</div>
          </div>
        </div>
      </section>

      <!-- ================= CALL TO ACTION SECTION ================= -->
      <section class="cta-section">
        <div class="cta-container">
          <div class="cta-icon">
            <Zap :size="48" />
          </div>
          <h2 class="cta-title">Ready to supercharge your calculations?</h2>

          <p class="cta-description">
            <template v-if="isAuthenticated">
              You're all set! Head to your dashboard to continue.
            </template>
            <template v-else-if="isGuest">
              You're in Guest mode — upgrade to Premium for unlimited features and permanent storage!
            </template>
            <template v-else>
              Create a free account for unlimited calculations, smart notes, weekly analytics,
              and full history management. No credit card required.
            </template>
          </p>

          <div class="cta-buttons">
            <template v-if="isAuthenticated">
              <button
                class="btn btn-primary-large"
                @click="goDashboard"
              >
                Go to Dashboard
                <ArrowRight :size="20" />
              </button>
            </template>

            <template v-else-if="isGuest">
              <button
                class="btn btn-primary-large"
                @click="goDashboard"
              >
                Continue in Dashboard
                <ArrowRight :size="20" />
              </button>

              <button
                class="btn btn-secondary-large"
                @click="upgradeFromGuest"
              >
                Upgrade to Premium
              </button>
            </template>

            <template v-else>
              <button
                class="btn btn-primary-large"
                @click="goRegister"
              >
                Get Premium Access Free
                <ArrowRight :size="20" />
              </button>

              <button
                class="btn btn-secondary-large"
                @click="continueAsGuest"
              >
                Try as Guest
              </button>
            </template>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import api from '@/services/api'

import {
  ArrowRight,
  CheckCircle2,
  XCircle,
  Calculator,
  History,
  FileText,
  Zap,
  Shield,
  User,
  Crown,
  TrendingUp,
  Trash2,
  Sparkles
} from 'lucide-vue-next'

export default {
  name: 'Welcome',
  components: {
    Navbar,
    Footer,
    ArrowRight,
    CheckCircle2,
    XCircle,
    Calculator,
    History,
    FileText,
    Zap,
    Shield,
    User,
    Crown,
    TrendingUp,
    Trash2,
    Sparkles
  },
  data() {
    return {
      username: localStorage.getItem('username') || null,
      authChecked: false
    }
  },
  computed: {
    isAuthenticated() {
      return !!this.username
    },
    isGuest() {
      return !this.isAuthenticated && localStorage.getItem('is_guest') === 'true'
    }
  },
  mounted() {
    this.syncAuth()
  },
  methods: {
    async syncAuth() {
      try {
        const res = await api.get('/auth/me/', { withCredentials: true })
        if (res.data.is_authenticated) {
          this.username = res.data.username
          localStorage.setItem('username', res.data.username)
          localStorage.removeItem('is_guest')
        } else {
          this.clearAuth()
        }
      } catch (err) {
        console.error('Auth check failed:', err)
        this.clearAuth()
      } finally {
        setTimeout(() => {
          this.authChecked = true
        }, 800)
      }
    },

    clearAuth() {
      this.username = null
      localStorage.removeItem('username')
    },

    goDashboard() {
      this.$router.push('/dashboard')
    },

    goRegister() {
      this.$router.push('/register')
    },

    continueAsGuest() {
      localStorage.setItem('is_guest', 'true')
      localStorage.removeItem('user')
      localStorage.removeItem('username')
      this.$router.push('/dashboard')
    },

    upgradeFromGuest() {
      localStorage.removeItem('is_guest')
      localStorage.removeItem('user')
      localStorage.removeItem('username')
      sessionStorage.clear()
      this.$router.push('/register')
    }
  }
}
</script>

<style scoped>
/* ================= LOADING SCREEN - Centered with Logo Inside Spinner ================= */
.loading-overlay {
  position: fixed;
  inset: 0;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loader-wrapper {
  position: relative;
  width: clamp(100px, 22vw, 140px);
  height: clamp(100px, 22vw, 140px);
  margin-bottom: 1.8rem;
}

.loader-ring {
  width: 100%;
  height: 100%;
  border: 8px solid #e2e8f0;
  border-top: 8px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1.3s cubic-bezier(0.645, 0.045, 0.355, 1) infinite;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.4);
}

.loader-icon-inside {
  color: #3b82f6;
  width: 55%;
  height: 55%;
  animation: pulse-inside 2.5s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse-inside {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.12); }
}

.loading-message {
  font-size: clamp(1rem, 4vw, 1.3rem);
  font-weight: 500;
  color: #475569;
  letter-spacing: 0.6px;
  max-width: 340px;
  margin: 0;
  line-height: 1.4;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.7s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* ================= GLOBAL PAGE STYLES ================= */
.welcome-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
  overflow-x: hidden;
}

/* ================= HERO SECTION ================= */
.hero-section {
  padding: clamp(5rem, 10vw, 8rem) 5vw clamp(6rem, 12vw, 10rem);
  position: relative;
  min-height: calc(100vh - 70px);
  display: flex;
  align-items: center;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 1200px;
  height: 600px;
  background: radial-gradient(circle at 50% 0%, rgba(59, 130, 246, 0.08) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

.hero-container {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.badge-wrapper {
  display: flex;
  justify-content: flex-start;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 50px;
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  font-weight: 600;
  font-size: 0.9rem;
  animation: badge-float 3s ease-in-out infinite;
}

.badge-icon {
  color: #3b82f6;
}

@keyframes badge-float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-4px); }
}

.hero-title {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.title-line {
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 700;
  line-height: 1.2;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.title-gradient {
  font-size: clamp(3rem, 6vw, 5rem);
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.03em;
}

.dot {
  color: #2563eb;
}

.hero-description {
  font-size: 1.2rem;
  line-height: 1.7;
  color: #475569;
  max-width: 600px;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.35);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.9);
  color: #0f172a;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.btn-primary-large {
  padding: 1.3rem 2.8rem;
  font-size: 1.15rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.btn-primary-large:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
}

.btn-secondary-large {
  padding: 1.3rem 2.8rem;
  font-size: 1.15rem;
  background: white;
  color: #0f172a;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.btn-secondary-large:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.trust-indicators {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #475569;
  font-size: 0.95rem;
}

.trust-item svg {
  color: #10b981;
}

/* ================= HERO VISUAL ================= */
.hero-visual {
  position: relative;
  height: 500px;
}

.visual-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(-50%, -50%) translateY(0px); }
  50% { transform: translate(-50%, -50%) translateY(-20px); }
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.card-dots {
  display: flex;
  gap: 6px;
}

.card-dots span {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.card-dots span:nth-child(1) { background: #ef4444; }
.card-dots span:nth-child(2) { background: #f59e0b; }
.card-dots span:nth-child(3) { background: #10b981; }

.card-title {
  font-weight: 600;
  color: #0f172a;
}

.card-content {
  padding: 2rem 1.5rem;
}

.calc-display {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.calc-operation {
  font-size: 1.1rem;
  color: #64748b;
  margin-bottom: 0.8rem;
}

.calc-result {
  font-size: 2.5rem;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 0.8rem;
}

.calc-note {
  font-size: 0.9rem;
  color: #7c3aed;
  font-style: italic;
  padding: 0.6rem 1rem;
  background: rgba(139, 92, 246, 0.08);
  border-radius: 8px;
  border-left: 3px solid #7c3aed;
  display: flex;
  align-items: center;
}

.calc-history {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1rem;
  background: rgba(59, 130, 246, 0.04);
  border-radius: 8px;
  font-size: 0.95rem;
}

.history-item span:first-child {
  color: #64748b;
}
.history-item span:last-child {
  font-weight: 600;
  color: #0f172a;
}

.float-card {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.8rem 1.2rem;
  background: white;
  border-radius: 50px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  font-size: 0.9rem;
  font-weight: 600;
  color: #0f172a;
  white-space: nowrap;
}

.float-card svg {
  color: #3b82f6;
}

.float-1 { top: 10%; right: -10%; animation: float-1 4s ease-in-out infinite; }
.float-2 { bottom: 30%; right: -15%; animation: float-2 5s ease-in-out infinite 0.5s; }
.float-3 { top: 60%; left: -12%; animation: float-3 4.5s ease-in-out infinite 1s; }

@keyframes float-1 { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
@keyframes float-2 { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
@keyframes float-3 { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }

/* ================= ACCESS COMPARISON SECTION ================= */
.comparison-section {
  padding: 100px 5vw;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
}

.section-container {
  max-width: 1320px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 5rem;
}

.section-badge {
  display: inline-block;
  padding: 8px 18px;
  border-radius: 50px;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.2);
  color: #7c3aed;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: clamp(2.5rem, 5vw, 3.5rem);
  font-weight: 800;
  line-height: 1.2;
  color: #0f172a;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.section-description {
  font-size: 1.25rem;
  color: #475569;
  max-width: 600px;
  margin: 0 auto;
}

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 2.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

.access-card {
  position: relative;
  padding: 3rem 2.5rem;
  background: white;
  border-radius: 24px;
  border: 2px solid rgba(0, 0, 0, 0.06);
  transition: all 0.4s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.guest-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
}

.premium-card {
  border: 2px solid #3b82f6;
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.15);
}

.premium-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 70px rgba(59, 130, 246, 0.25);
}

.premium-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  padding: 6px 20px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.access-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.access-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: white;
}

.guest-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.premium-icon {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.access-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.access-subtitle {
  font-size: 1rem;
  color: #64748b;
  margin-bottom: 2rem;
}

.access-features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
  font-size: 0.95rem;
}

.feature-item.enabled {
  color: #0f172a;
}

.feature-item.enabled svg {
  color: #10b981;
  flex-shrink: 0;
  margin-top: 2px;
}

.feature-item.disabled {
  color: #94a3b8;
}

.feature-item.disabled svg {
  color: #cbd5e1;
}

.btn-access {
  width: 100%;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  border: 2px solid rgba(0, 0, 0, 0.1);
  background: white;
  color: #0f172a;
}

.btn-access:hover {
  background: #0f172a;
  color: white;
  transform: translateY(-2px);
}

.premium-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
}

.premium-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.35);
}

/* ================= FEATURES SECTION ================= */
.features-section {
  padding: 100px 5vw;
  background: white;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.feature-card {
  padding: 2.5rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%);
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: all 0.4s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
  border-color: rgba(59, 130, 246, 0.2);
}

.feature-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  color: white;
}

.feature-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 1rem;
}

.feature-description {
  font-size: 1rem;
  line-height: 1.6;
  color: #475569;
}

/* ================= STATS SECTION ================= */
.stats-section {
  padding: 80px 5vw;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stats-grid {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 3rem;
}

.stat-card {
  text-align: center;
}

.stat-number {
  font-size: 3.5rem;
  font-weight: 900;
  color: white;
  margin-bottom: 0.5rem;
  line-height: 1;
}

.stat-label {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.85);
  font-weight: 500;
}

/* ================= CTA SECTION ================= */
.cta-section {
  padding: 100px 5vw;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.cta-container {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
  padding: 5rem 3rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 30px;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.cta-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.cta-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.cta-description {
  font-size: 1.25rem;
  color: #475569;
  margin-bottom: 2.5rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.7;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* ================= RESPONSIVE DESIGN ================= */
@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 60px;
  }

  .hero-visual {
    height: 400px;
  }

  .float-card {
    display: none;
  }

  .comparison-grid {
    grid-template-columns: 1fr;
    max-width: 500px;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 80px 5vw 60px;
  }

  .hero-content {
    gap: 1.5rem;
  }

  .hero-actions {
    flex-direction: column;
    width: 100%;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .trust-indicators {
    flex-direction: column;
    gap: 0.8rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }

  .stat-number {
    font-size: 2.5rem;
  }

  .cta-container {
    padding: 3rem 2rem;
  }

  .cta-buttons {
    flex-direction: column;
  }

  .btn-primary-large,
  .btn-secondary-large {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .visual-card {
    max-width: 100%;
  }

  .calc-result {
    font-size: 2rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .comparison-grid {
    grid-template-columns: 1fr;
  }

  .loading-message {
    font-size: 1rem;
    max-width: 280px;
  }
}
</style>