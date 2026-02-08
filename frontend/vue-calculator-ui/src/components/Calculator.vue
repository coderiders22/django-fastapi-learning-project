<template>
  <div class="calculator-wrapper">
    <!-- 
      Professional Info Banner
      This banner dynamically shows guest vs premium features
      Uses computed 'isGuest' to determine user status
    -->
    <div class="info-banner" :class="isGuest ? 'guest-mode' : 'premium-mode'">
      <div class="banner-icon">
        <!-- Conditional icon based on user status -->
        <ShieldAlert v-if="isGuest" :size="24" />
        <CheckCircle2 v-else :size="24" />
      </div>
      <div class="banner-content">
        <div class="banner-title">
          {{ isGuest ? 'Guest Mode Active' : 'Premium Access Active' }}
        </div>
        <div class="banner-description" v-if="isGuest">
          Limited access features enabled
        </div>
        <div class="banner-description" v-else>
        Congratulations! You now have full access to all premium features.
        </div>
        
        <!-- 
          Feature list shows different capabilities based on user status
          This helps users understand what they can/cannot do
        -->
        <div class="feature-list" v-if="isGuest">
          <div class="feature-item success">
            <CheckCircle2 :size="16" />
            <span>View last 10 calculations</span>
          </div>
          <div class="feature-item success">
            <CheckCircle2 :size="16" />
            <span>Add notes to 2 calculations</span>
          </div>
          <div class="feature-item disabled">
            <XCircle :size="16" />
            <span>Cannot clear history</span>
          </div>
          <div class="feature-item disabled">
            <XCircle :size="16" />
            <span>Cannot delete individual items</span>
          </div>
        </div>
        <div class="feature-list" v-else>
          <div class="feature-item success">
            <CheckCircle2 :size="16" />
            <span>Unlimited calculations</span>
          </div>
          <div class="feature-item success">
            <CheckCircle2 :size="16" />
            <span>Unlimited notes</span>
          </div>
          <div class="feature-item success">
            <CheckCircle2 :size="16" />
            <span>Full history access</span>
          </div>
        </div>
      </div>
      
      <!-- CTA button for guest users to upgrade -->
      <button v-if="isGuest" class="upgrade-button" @click="exitGuestAndLogin">
        <span>Login for Full Access</span>
        <ArrowRight :size="18" />
      </button>
    </div>

    <!-- 
      Display Section
      Shows current calculation expression in a clean, readable format
      Uses null-safe rendering with ?? operator
    -->
    <div class="calculator-display">
      <div class="display-header">
        <div class="display-label">
          <CalcIcon :size="16" />
          <span>Current Calculation</span>
        </div>
        <!-- Clear button with rotation animation on hover -->
        <button
          class="clear-btn"
          @click="clearAll"
          title="Clear inputs"
          :disabled="loading"
        >
          <RotateCcw :size="16" />
        </button>
      </div>
      <div class="expression-display">
        <!-- Show calculation expression or placeholder -->
        <span v-if="a !== null || b !== null" class="expression-text">
          {{ a ?? 0 }} {{ op }} {{ b ?? 0 }}
        </span>
        <span v-else class="placeholder-text">
          Enter your calculation
        </span>
      </div>
    </div>

    <!-- 
      Inputs Section
      All calculator inputs grouped together for better UX
      Each input has proper labels and icons for accessibility
    -->
    <div class="calculator-inputs">
      <!-- First operand input with ref for programmatic focus -->
      <div class="input-group">
        <label class="input-label">
          <Hash :size="14" /> First Number
        </label>
        <input
          ref="firstInput"
          v-model="a"
          type="number"
          class="input-field"
          placeholder="0"
          @input="onInputA"
          @keyup.enter="focusSecondInput"
        />
      </div>

      <!-- 
        Operator selection buttons
        Grid layout for visual balance and easy selection
      -->
      <div class="operator-group">
        <label class="input-label">Operator</label>
        <div class="operator-buttons">
          <button
            v-for="o in operators"
            :key="o.value"
            class="operator-btn"
            :class="{ active: op === o.value }"
            @click="op = o.value"
          >
            <component :is="o.icon" :size="20" />
            <span>{{ o.display }}</span>
          </button>
        </div>
      </div>

      <!-- Second operand input with Enter key support -->
      <div class="input-group">
        <label class="input-label">
          <Hash :size="14" /> Second Number
        </label>
        <input
          ref="secondInput"
          v-model="b"
          type="number"
          class="input-field"
          placeholder="0"
          @input="onInputB"
          @keyup.enter="calculate"
        />
      </div>

      <!-- 
        Note Input
        Optional field for users to add context to their calculations
        Max 500 chars with real-time character counter
      -->
      <div class="input-group">
        <label class="input-label">
          <FileText :size="14" /> Note (Optional)
        </label>
        <textarea
          v-model="note"
          class="note-field"
          placeholder="Add a note about this calculation... (max 500 characters)"
          maxlength="500"
          rows="2"
        ></textarea>
        <div class="char-count">{{ note.length }}/500</div>
      </div>
    </div>

    <!-- 
      Calculate Button
      Disabled when inputs are invalid or calculation is in progress
      Shows loading spinner during API call
    -->
    <button
      class="calculate-btn"
      :disabled="loading || !canCalculate"
      @click="calculate"
    >
      <span v-if="loading" class="btn-content">
        <span class="spinner"></span>
        Calculating...
      </span>
      <span v-else class="btn-content">
        <Zap :size="18" />
        Calculate
        <ArrowRight :size="18" />
      </span>
    </button>

    <!-- 
      Result Section
      Only shows after successful calculation
      Includes copy and clear functionality
      Transition animation for smooth appearance
    -->
    <transition name="result">
      <div v-if="result !== null" class="result-section">
        <div class="result-header">
          <CheckCircle2 :size="20" />
          Result
        </div>
        <div class="result-value">
          {{ formatResult(result) }}
        </div>
        <div class="result-actions">
          <button class="result-action-btn" @click="copyResult">
            <Copy :size="16" />
            {{ copied ? 'Copied!' : 'Copy' }}
          </button>
          <button class="result-action-btn" @click="clearResult">
            <X :size="16" />
            Clear
          </button>
        </div>
      </div>
    </transition>

    <!-- 
      Modal Component
      Shows error/warning messages to user
      Controlled by showModal flag
    -->
    <Modal
      v-if="showModal"
      :text="modalText"
      :type="modalType"
      @close="showModal = false"
    />
  </div>
</template>

<script>
// Import API service for backend communication
import api from '@/services/api'
import Modal from '@/components/Modal.vue'

// Import all required Lucide icons
import {
  Calculator as CalcIcon,
  Hash,
  Zap,
  ArrowRight,
  CheckCircle2,
  Copy,
  X,
  RotateCcw,
  Plus,
  Minus,
  Asterisk,
  Divide,
  ShieldAlert,
  XCircle,
  FileText
} from 'lucide-vue-next'

export default {
  name: 'Calculator',
  props: {},
  components: {
    Modal,
    CalcIcon,
    Hash,
    Zap,
    ArrowRight,
    CheckCircle2,
    Copy,
    X,
    RotateCcw,
    Plus,
    Minus,
    Asterisk,
    Divide,
    ShieldAlert,
    XCircle,
    FileText
  },
  data() {
    return {
      // Calculator operands - null instead of 0 to distinguish empty state
      a: null,
      b: null,
      
      // Current operator - defaults to addition
      op: '+',
      
      // Stores calculation result from backend
      result: null,
      
      // Loading state for async operations
      loading: false,
      
      // Modal control flags
      showModal: false,
      modalText: '',
      modalType: 'error',
      
      // Clipboard copy feedback
      copied: false,
      
      // Current user info - loaded from localStorage first for instant UI
      username: localStorage.getItem('username') || null,
      
      // Optional note for calculation (max 500 chars)
      note: '', 
      
      // Operator configuration with icons and display symbols
      operators: [
        { value: '+', display: '+', icon: 'Plus' },
        { value: '-', display: '−', icon: 'Minus' },
        { value: '*', display: '×', icon: 'Asterisk' },
        { value: '/', display: '÷', icon: 'Divide' }
      ]
    }
  },
  computed: {
    /**
     * Checks if both operands are entered
     * Used to enable/disable calculate button
     */
    canCalculate() {
      return this.a !== null && this.b !== null
    },
    
    /**
     * Determines if user is in guest mode
     * Checks both authentication status and localStorage flag
     */
    isGuest() {
      return !this.username && localStorage.getItem('is_guest') === 'true'
    }
  },
  methods: {
    /**
     * Exits guest mode and redirects to login page
     * Clears guest flag from localStorage
     */
    exitGuestAndLogin() {
      // Remove guest flag
      localStorage.removeItem('is_guest')
      // Redirect to login page
      this.$router.push('/login')
    },

    /**
     * Fetches current user data from backend
     * Called on mount and route changes to keep auth state updated
     */
    async fetchUser() {
      try {
        const res = await api.get('/auth/me/', { withCredentials: true })
        
        if (res.data.is_authenticated) {
          this.username = res.data.username
          // Keep localStorage in sync
          localStorage.setItem('username', res.data.username)
          // Remove guest flag if user is authenticated
          localStorage.removeItem('is_guest')
        } else {
          this.username = null
          localStorage.removeItem('username')
        }
      } catch (error) {
        // If API fails, treat as non-authenticated
        this.username = null
        localStorage.removeItem('username')
      }
    },
    
    /**
     * Handles first operand input
     * Converts empty string to null for proper validation
     */
    onInputA(e) {
      this.a = e.target.value === '' ? null : parseFloat(e.target.value)
    },
    
    /**
     * Handles second operand input
     * Converts empty string to null for proper validation
     */
    onInputB(e) {
      this.b = e.target.value === '' ? null : parseFloat(e.target.value)
    },
    
    /**
     * Main calculation method
     * Sends request to Django backend and handles response/errors
     * Validates division by zero before sending request
     */
    async calculate() {
      // Early return if inputs not valid
      if (!this.canCalculate) return
      
      // Client-side validation for division by zero
      if (this.op === '/' && this.b === 0) {
        this.modalText = 'Cannot divide by zero.'
        this.modalType = 'error'
        this.showModal = true
        return
      }
      
      // Set loading state and clear previous result
      this.loading = true
      this.result = null
      
      try {
        // Send calculation request to Django REST API
        const res = await api.post('/calculate/', {
          operand1: this.a,
          operand2: this.b,
          operator: this.op,
          note: this.note  // Include optional note
        })
        
        // Store result from backend
        this.result = res.data.result
        
        // Clear note after successful calculation
        this.note = ''
        
        // Emit event to parent (for history refresh)
        this.$emit('calculated')
        
      } catch (err) {
        // Handle specific error cases
        if (err.response?.status === 403) {
          // Guest limit reached
          this.modalText = err.response.data.error || 'Limit reached. Login to unlock full access.'
          this.modalType = 'warning'
        } else {
          // Generic error
          this.modalText = err.response?.data?.error || 'Calculation failed.'
          this.modalType = 'error'
        }
        this.showModal = true
        
      } finally {
        // Always stop loading spinner
        this.loading = false
      }
    },
    
    /**
     * Formats result with proper number formatting
     * Uses Intl API for locale-aware number display
     * Limits to 10 decimal places to avoid floating point issues
     */
    formatResult(value) {
      return new Intl.NumberFormat('en-US', {
        maximumFractionDigits: 10
      }).format(value)
    },
    
    /**
     * Copies result to clipboard
     * Shows temporary "Copied!" feedback for 2 seconds
     */
    async copyResult() {
      await navigator.clipboard.writeText(String(this.result))
      this.copied = true
      setTimeout(() => (this.copied = false), 2000)
    },
    
    /**
     * Clears just the result display
     * Keeps input values intact
     */
    clearResult() {
      this.result = null
    },
    
    /**
     * Resets entire calculator to initial state
     * Also focuses first input for quick restart
     */
    clearAll() {
      this.a = null
      this.b = null
      this.op = '+'
      this.result = null
      this.note = ''
      // Focus first input for better UX
      this.$refs.firstInput?.focus()
    },
    
    /**
     * Keyboard navigation helper
     * Moves focus from first to second input on Enter key
     */
    focusSecondInput() {
      this.$refs.secondInput?.focus()
    }
  },
  
  /**
   * Component lifecycle hook
   * Fetches user data when component mounts
   */
  async mounted() {
    await this.fetchUser()
  },
  
  /**
   * Watch for route changes
   * Refetch user data when navigating (e.g., after login/logout)
   */
  watch: {
    '$route'() {
      this.fetchUser()
    }
  }
}
</script>

<style scoped>
/* Calculator main wrapper */
.calculator-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ==================== Info Banner Styles ==================== */
/* 
  Professional banner showing user status and features
  Uses different color schemes for guest vs premium modes
*/
.info-banner {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  padding: 1.5rem;
  border-radius: 16px;
  backdrop-filter: blur(12px);
  border: 1px solid;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  animation: slideDown 0.5s ease-out;
}

/* Smooth slide-down entrance animation */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Guest mode styling - amber/orange theme */
.info-banner.guest-mode {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.15), rgba(245, 158, 11, 0.15));
  border-color: rgba(245, 158, 11, 0.3);
}

/* Premium mode styling - green theme */
.info-banner.premium-mode {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.15));
  border-color: rgba(16, 185, 129, 0.3);
}

/* Subtle lift effect on hover */
.info-banner:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

/* Banner icon container */
.banner-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  transition: transform 0.3s ease;
}

.guest-mode .banner-icon {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: white;
}

.premium-mode .banner-icon {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

/* Fun rotation effect on banner hover */
.info-banner:hover .banner-icon {
  transform: scale(1.1) rotate(5deg);
}

/* Banner text content */
.banner-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.banner-title {
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.guest-mode .banner-title {
  color: #92400e;
}

.premium-mode .banner-title {
  color: #065f46;
}

.banner-description {
  font-size: 0.9rem;
  font-weight: 500;
  opacity: 0.85;
  line-height: 1.5;
}

.guest-mode .banner-description {
  color: #78350f;
}

.premium-mode .banner-description {
  color: #047857;
}

/* Feature list showing what user can/cannot do */
.feature-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-top: 0.25rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 0.4rem 0;
  transition: transform 0.2s ease;
}

/* Subtle slide-in effect on hover */
.feature-item:hover {
  transform: translateX(4px);
}

.feature-item.success {
  color: #166534;
}

.feature-item.disabled {
  color: #92400e;
  opacity: 0.8;
}

.premium-mode .feature-item.success {
  color: #065f46;
}

/* Upgrade/Login CTA button */
.upgrade-button {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
  white-space: nowrap;
  align-self: flex-start;
}

.upgrade-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(245, 158, 11, 0.35);
  background: linear-gradient(135deg, #d97706, #b45309);
}

.upgrade-button:active {
  transform: translateY(0);
}

/* ==================== Display Section ==================== */
/* Shows current calculation expression */
.calculator-display {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.08));
  border: 1px solid rgba(59, 130, 246, 0.15);
  border-radius: 16px;
  padding: 1.5rem;
}

.display-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.display-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 600;
}

/* Clear button with rotation animation */
.clear-btn {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: white;
  color: var(--text-primary);
  transform: rotate(180deg);
}

/* Expression display area */
.expression-display {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  min-height: 2.5rem;
  display: flex;
  align-items: center;
}

.expression-text {
  color: var(--primary);
}

.placeholder-text {
  color: var(--text-muted);
  font-size: 1.2rem;
  font-weight: 500;
}

/* ==================== Input Section ==================== */
.calculator-inputs {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

/* Input labels with icons */
.input-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-primary);
  font-size: 0.9rem;
  font-weight: 600;
}

/* Number input fields */
.input-field {
  width: 100%;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

/* Focus state with blue glow */
.input-field:focus {
  outline: none;
  background: white;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.input-field::placeholder {
  color: var(--text-muted);
  font-weight: 400;
}

/* ==================== Note Field ==================== */
/* Textarea for calculation notes */
.note-field {
  width: 100%;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-primary);
  font-family: inherit;
  resize: vertical;
  min-height: 60px;
  transition: all 0.3s ease;
}

.note-field:focus {
  outline: none;
  background: white;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.note-field::placeholder {
  color: var(--text-muted);
  font-weight: 400;
}

/* Character counter for note field */
.char-count {
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-align: right;
  margin-top: 0.25rem;
}

/* ==================== Operator Buttons ==================== */
.operator-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

/* Grid layout for 4 operators */
.operator-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.operator-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  padding: 1rem 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 1.5rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.operator-btn:hover {
  background: white;
  border-color: rgba(59, 130, 246, 0.2);
  transform: translateY(-2px);
}

/* Active operator highlighted in blue */
.operator-btn.active {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  border-color: var(--primary);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.operator-btn span {
  font-size: 0.75rem;
  font-weight: 600;
}

/* ==================== Calculate Button ==================== */
.calculate-btn {
  width: 100%;
  padding: 1.25rem;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
  margin-top: 0.5rem;
}

.calculate-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

/* Disabled state when inputs invalid or loading */
.calculate-btn:disabled {
  background: linear-gradient(135deg, #cbd5e1, #94a3b8);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

/* Loading spinner animation */
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

/* ==================== Result Section ==================== */
.result-section {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(5, 150, 105, 0.08));
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: var(--success);
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

/* Large, prominent result display */
.result-value {
  font-size: 3rem;
  font-weight: 800;
  color: var(--success);
  margin-bottom: 1rem;
  word-break: break-all;
  line-height: 1.2;
}

.result-actions {
  display: flex;
  gap: 0.75rem;
}

/* Copy and Clear buttons */
.result-action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 10px;
  color: var(--success);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.result-action-btn:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
}

/* ==================== Animations ==================== */
/* Vue transition for result appearance/disappearance */
.result-enter-active,
.result-leave-active {
  transition: all 0.4s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.result-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.result-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

/* ==================== Responsive Design ==================== */
/* Tablet and below - adjust banner layout */
@media (max-width: 768px) {
  .info-banner {
    flex-direction: column;
    gap: 1rem;
  }

  .banner-icon {
    width: 40px;
    height: 40px;
  }

  .upgrade-button {
    width: 100%;
    justify-content: center;
  }

  /* Stack operators in 2x2 grid on smaller screens */
  .operator-buttons {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Mobile - further size adjustments */
@media (max-width: 640px) {
  .expression-display {
    font-size: 1.5rem;
  }

  .result-value {
    font-size: 2.5rem;
  }

  /* Stack result action buttons vertically */
  .result-actions {
    flex-direction: column;
  }

  .feature-list {
    gap: 0.5rem;
  }

  .feature-item {
    font-size: 0.8rem;
  }
}
</style>