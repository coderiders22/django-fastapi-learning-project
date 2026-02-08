<!-- src/views/Dashboard.vue -->
<template>
  <div class="dashboard-wrapper">
    <!-- Top Navbar: Contains logo, navigation, and user menu -->
    <Navbar />
    
    <main class="dashboard-main">
      <div class="dashboard-container">
        <!-- ================= HEADER SECTION ================= -->
        <!-- Displays personalized greeting and user statistics -->
        <header class="dashboard-header">
          <div class="header-content">
            <div class="header-text">
              <!-- Dynamic greeting badge based on time of day -->
              <div class="greeting-badge">
                <Sparkles :size="16" />
                <span>{{ greetingTime }}</span>
              </div>
              <!-- Personalized welcome message with username -->
              <h1 class="header-title">
                Welcome back,
                <span class="user-highlight">{{ username }}</span>
              </h1>
              <p class="header-subtitle">
                Your professional calculation workspace is ready
              </p>
            </div>
            <!-- Statistics cards showing user activity -->
            <div class="header-stats">
              <!-- Total calculations card -->
              <div class="stat-card">
                <div class="stat-icon">
                  <CalcIcon :size="20" />
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ totalCalculations }}</div>
                  <div class="stat-label">Total Calculations</div>
                </div>
              </div>
              <!-- This week's calculations card -->
              <div class="stat-card">
                <div
                  class="stat-icon"
                  style="background: linear-gradient(135deg,#10b981,#059669)"
                >
                  <TrendingUp :size="20" />
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ weekCalculations }}</div>
                  <div class="stat-label">This Week</div>
                </div>
              </div>
            </div>
          </div>
        </header>

        <!-- ================= QUICK ACTIONS SECTION ================= -->
        <!-- Provides shortcuts to main features -->
        <section class="quick-actions">
          <div class="section-header">
            <Zap :size="20" />
            <h2>Quick Actions</h2>
          </div>
          <div class="actions-grid">
            <!-- Action card: Focus calculator input -->
            <button class="action-card" @click="focusCalculator">
              <div class="action-icon">
                <Plus :size="24" />
              </div>
              <div class="action-content">
                <div class="action-title">New Calculation</div>
                <div class="action-subtitle">Start a fresh calculation</div>
              </div>
            </button>
            <!-- Action card: Scroll to history section -->
            <button class="action-card" @click="scrollToHistory">
              <div
                class="action-icon"
                style="background: linear-gradient(135deg,#8b5cf6,#7c3aed)"
              >
                <HistoryIcon :size="24" />
              </div>
              <div class="action-content">
                <div class="action-title">View History</div>
                <div class="action-subtitle">Browse past calculations</div>
              </div>
            </button>
          </div>
        </section>

        <!-- ================= MAIN CONTENT GRID ================= -->
        <!-- Two-column layout: Calculator on left, History on right -->
        <section class="content-grid">
          <!-- Calculator Section -->
          <div class="section-card">
            <div class="card-header">
              <div class="card-header-left">
                <div class="card-icon">
                  <CalcIcon :size="20" />
                </div>
                <h3>Calculator</h3>
              </div>
            </div>
            <div class="card-content">
              <!-- Calculator component with ref for programmatic access -->
              <!-- @calculated event triggers when a new calculation is made -->
              <Calculator
                ref="calculatorRef"
                @calculated="onCalculated"
              />
            </div>
          </div>

          <!-- History Section with ref for smooth scrolling -->
          <div class="section-card" ref="historySection">
            <div class="card-header">
              <div class="card-header-left">
                <div
                  class="card-icon"
                  style="background: linear-gradient(135deg,#8b5cf6,#7c3aed)"
                >
                  <HistoryIcon :size="20" />
                </div>
                <h3>Recent History</h3>
              </div>
            </div>
            <div class="card-content history-content">
              <!-- History component receives isGuest prop to control features -->
              <History ref="historyRef" :isGuest="isGuest" />
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- Footer: Contains copyright and links -->
    <Footer />
  </div>
</template>

<script>
// Import layout components
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'

// Import feature components
import Calculator from '@/components/Calculator.vue'
import History from '@/components/History.vue'

// Import API service for backend communication
import api from '@/services/api'

// Import Lucide icons for UI elements
import {
  Calculator as CalcIcon,
  Sparkles,
  TrendingUp,
  Zap,
  Plus,
  History as HistoryIcon
} from 'lucide-vue-next'

export default {
  name: 'Dashboard',
  
  components: {
    Navbar,
    Footer,
    Calculator,
    History,
    CalcIcon,
    Sparkles,
    TrendingUp,
    Zap,
    Plus,
    HistoryIcon
  },
  
  data() {
    return {
      username: localStorage.getItem('username') || 'Guest',  // Load from localStorage first
      isGuest: !localStorage.getItem('username') && localStorage.getItem('is_guest') === 'true',
      totalCalculations: 0,        // Total number of calculations made
      weekCalculations: 0          // Calculations made in last 7 days
    }
  },
  
  computed: {
    /**
     * Returns dynamic greeting based on current time
     * Morning: 00:00 - 11:59
     * Afternoon: 12:00 - 17:59
     * Evening: 18:00 - 23:59
     */
    greetingTime() {
      const hour = new Date().getHours()
      if (hour < 12) return 'Good Morning'
      if (hour < 18) return 'Good Afternoon'
      return 'Good Evening'
    }
  },
  
  /**
   * Lifecycle hook: Called when component is mounted to DOM
   * Fetches user data and statistics on page load
   */
  async mounted() {
    await this.fetchUser()
    await this.refreshStats()
  },
  
  methods: {
    /**
     * Fetches current user authentication status
     * Sets username and guest flag based on response
     * Falls back to guest mode if request fails
     */
    async fetchUser() {
      try {
        const res = await api.get('/auth/me/', {
          withCredentials: true
        })
        if (res.data.is_authenticated) {
          this.username = res.data.username
          this.isGuest = false
          // Keep localStorage in sync
          localStorage.setItem('username', res.data.username)
        } else {
          this.username = 'Guest'
          this.isGuest = true
          localStorage.removeItem('username')
        }
      } catch (err) {
        // If authentication check fails, default to guest mode
        this.username = 'Guest'
        this.isGuest = true
        localStorage.removeItem('username')
      }
    },

    /**
     * Fetches calculation statistics from history
     * Calculates total and weekly calculation counts
     * Includes safety check to ensure data is array
     */
    async refreshStats() {
      try {
        const res = await api.get('/history/', {
          withCredentials: true
        })

        // Safety check: Ensure response is array to prevent errors
        // This prevents crashes if API returns unexpected data format
        const history = Array.isArray(res.data) ? res.data : []

        this.totalCalculations = history.length

        // Calculate this week's calculations (last 7 days)
        const now = new Date()
        const sevenDaysAgo = new Date(
          now.getTime() - (7 * 24 * 60 * 60 * 1000)
        )

        // Filter items created within last 7 days
        this.weekCalculations = history.filter(item => {
          if (!item.created_at) return false
          const itemDate = new Date(item.created_at)
          return itemDate >= sevenDaysAgo
        }).length

      } catch (err) {
        console.error('Failed to load stats:', err)
        // Reset stats to zero if fetch fails
        this.totalCalculations = 0
        this.weekCalculations = 0
      }
    },

    /**
     * Event handler called when new calculation is completed
     * Updates statistics and refreshes history display
     * Optimistic UI update for better perceived performance
     */
    onCalculated() {
      // Immediately increment counters for instant feedback
      this.totalCalculations++
      this.weekCalculations++
      
      // Refresh history component to show new calculation
      // Optional chaining (?.) prevents errors if ref not available
      this.$refs.historyRef?.fetchHistory?.()
      
      // Fetch accurate stats from server in background
      this.refreshStats()
    },

    /**
     * Programmatically focuses calculator input field
     * Uses optional chaining to safely navigate DOM
     * Provides keyboard-first user experience
     */
    focusCalculator() {
      this.$refs.calculatorRef?.$el
        ?.querySelector('input')
        ?.focus()
    },

    /**
     * Smoothly scrolls to history section
     * Uses native scrollIntoView for smooth animation
     * Improves navigation on single-page layout
     */
    scrollToHistory() {
      this.$refs.historySection?.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      })
    }
  }
}
</script>

<style scoped>
/* Main wrapper: Full viewport height with gradient background */
.dashboard-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  display: flex;
  flex-direction: column;
  padding-top: 70px; /* Offset for fixed navbar */
}

/* Main content area with flex growth */
.dashboard-main {
  flex: 1;
  padding: 40px 0;
}

/* Container with max-width for content alignment */
.dashboard-container {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 60px;
  width: 100%;
}

/* ================= HEADER STYLES ================= */
.dashboard-header {
  margin-bottom: 3rem;
}

/* Header card with glassmorphism effect */
.header-content {
  background: white;
  border-radius: 24px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 3rem 2.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

/* Greeting badge with primary color and uppercase text */
.greeting-badge {
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
  letter-spacing: 0.5px; /* Improved readability */
}

/* Large, bold header title with tight letter spacing */
.header-title {
  font-size: 3rem;
  font-weight: 900;
  color: #1e293b;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em; /* Tighter spacing for large text */
}

.user-highlight {
  color: #1e293b;
}

/* Subtitle with muted color */
.header-subtitle {
  font-size: 1.15rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 3rem;
}

/* Statistics grid: Two equal columns */
.header-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

/* Stat card with hover effect */
.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: #f8fafc;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 16px;
  transition: all 0.3s ease;
}

/* Lift effect on hover for interactivity */
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

/* Icon container with gradient background */
.stat-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0; /* Prevents icon from shrinking */
}

.stat-info {
  display: flex;
  flex-direction: column;
}

/* Large stat value with bold weight */
.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.95rem;
  color: #64748b;
  font-weight: 500;
}

/* ================= QUICK ACTIONS STYLES ================= */
.quick-actions {
  margin-bottom: 3rem;
}

/* Section header with icon */
.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.section-header svg {
  color: #1e293b;
}

.section-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

/* Responsive grid for action cards */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* Action card: Clickable button with smooth transitions */
.action-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1); /* Smooth easing */
  text-align: left;
}

/* Hover effect: Lift and highlight */
.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: rgba(59, 130, 246, 0.15);
}

/* Icon container for action cards */
.action-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.action-content {
  display: flex;
  flex-direction: column;
}

.action-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.action-subtitle {
  font-size: 0.95rem;
  color: #64748b;
}

/* ================= CONTENT GRID STYLES ================= */
/* Two-column layout: Calculator (60%) and History (40%) */
.content-grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
}

/* Section card: Container for calculator and history */
.section-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  overflow: hidden; /* Prevents content overflow */
}

/* Card header with bottom border */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.card-header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Card icon with gradient */
.card-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-header h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

/* Card content area with padding */
.card-content {
  padding: 2rem;
}

/* History content: Scrollable area with max height */
.history-content {
  max-height: 500px;
  overflow-y: auto;
}

/* ================= RESPONSIVE DESIGN ================= */
/* Tablet: Single column layout */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .header-stats {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }
}

/* Mobile landscape: Reduced padding */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 0 30px;
  }

  .header-content {
    padding: 2rem 1.5rem;
  }

  .card-header {
    padding: 1.25rem 1.5rem;
  }

  .card-content {
    padding: 1.5rem;
  }
}

/* Mobile portrait: Minimal padding and smaller text */
@media (max-width: 480px) {
  .dashboard-main {
    padding: 20px 0 40px;
  }

  .dashboard-container {
    padding: 0 20px;
  }

  .header-content {
    padding: 1.5rem;
  }

  .header-title {
    font-size: 2rem;
  }

  .greeting-badge {
    font-size: 0.8rem;
    padding: 6px 12px;
  }

  .action-card {
    padding: 1.25rem;
  }

  .action-icon {
    width: 48px;
    height: 48px;
  }
}
</style>