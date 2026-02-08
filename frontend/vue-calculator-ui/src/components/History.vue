<!-- components/History.vue -->
<template>
  <div class="history-wrapper">
    <!-- Header Section: Displays total count and action buttons -->
    <div class="history-header">
      <div class="history-count">
        <span class="count-number">{{ history.length }}</span>
        <span class="count-label">calculations</span>
      </div>
      <div class="header-actions">
        <!-- Refresh button with loading animation -->
        <button
          class="action-button"
          :class="{ spinning: loading }"
          @click="fetchHistory"
          :disabled="loading"
          title="Refresh history"
        >
          <RefreshCw :size="16" />
        </button>
        <!-- Clear all button - only visible for authenticated users -->
        <button
          v-if="!isGuest && history.length > 0"
          class="action-button clear"
          @click="confirmClear"
          title="Clear all history"
        >
          <Trash2 :size="16" />
        </button>
      </div>
    </div>

    <!-- Loading State: Shows spinner while fetching data -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading history...</p>
    </div>

    <!-- Empty State: Displayed when no calculations exist -->
    <div v-else-if="history.length === 0" class="empty-state">
      <div class="empty-icon">
        <Calculator :size="32" />
      </div>
      <h3 class="empty-title">No calculations yet</h3>
      <p class="empty-description">
        Your calculation history will appear here once you start calculating.
      </p>
    </div>

    <!-- History List: Renders calculation items with smooth transitions -->
    <transition-group
      v-else
      name="list"
      tag="div"
      class="history-list"
    >
      <div
        v-for="item in history"
        :key="item.id"
        class="history-item"
      >
        <div class="item-content">
          <!-- Icon indicator for each calculation -->
          <div class="item-icon">
            <Calculator :size="18" />
          </div>
          <div class="item-details">
            <!-- Expression display: operand1 operator operand2 -->
            <div class="expression">
              <span class="operand">{{ formatNumber(item.operand1) }}</span>
              <span class="operator">{{ formatOperator(item.operator) }}</span>
              <span class="operand">{{ formatNumber(item.operand2) }}</span>
            </div>
            <!-- Result line with equal sign -->
            <div class="result-line">
              <Equal :size="14" />
              <span class="result">{{ formatNumber(item.result) }}</span>
            </div>
            <!-- Note display: Shows user-added note if exists -->
            <div v-if="item.note" class="note-display">
              <FileText :size="12" />
              <span>{{ item.note }}</span>
            </div>
          </div>
        </div>
        <!-- Action buttons: Copy and Delete (visible on hover) -->
        <div class="item-actions">
          <button
            class="item-action-btn"
            @click="copyResult(item.result)"
            title="Copy result"
          >
            <Copy :size="16" />
          </button>
          <button
            v-if="!isGuest"
            class="item-action-btn delete"
            @click="confirmDelete(item.id)"
            title="Delete calculation"
          >
            <Trash2 :size="16" />
          </button>
        </div>
      </div>
    </transition-group>

    <!-- Clear All Confirmation Modal -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="showClearModal" class="modal-overlay" @click.self="showClearModal = false">
          <div class="modal-content">
            <div class="modal-icon warning">
              <AlertTriangle :size="28" />
            </div>
            <h3 class="modal-title">Clear All History?</h3>
            <p class="modal-description">
              This will permanently delete all your calculation history. This action cannot be undone.
            </p>
            <div class="modal-actions">
              <button class="modal-btn cancel" @click="showClearModal = false">
                <X :size="18" />
                Cancel
              </button>
              <button class="modal-btn confirm" @click="clearAll">
                <Trash2 :size="18" />
                Clear All
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- Delete Single Item Confirmation Modal -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
          <div class="modal-content">
            <div class="modal-icon warning">
              <AlertTriangle :size="28" />
            </div>
            <h3 class="modal-title">Delete Calculation?</h3>
            <p class="modal-description">
              Are you sure you want to delete this calculation? This action cannot be undone.
            </p>
            <div class="modal-actions">
              <button class="modal-btn cancel" @click="showDeleteModal = false">
                <X :size="18" />
                Cancel
              </button>
              <button class="modal-btn confirm" @click="deleteItem">
                <Trash2 :size="18" />
                Delete
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- Success Modal: Shows feedback after successful operations -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="showSuccessModal" class="modal-overlay" @click.self="showSuccessModal = false">
          <div class="modal-content">
            <div class="modal-icon success">
              <CheckCircle2 :size="32" />
            </div>
            <h3 class="modal-title">Success!</h3>
            <p class="modal-description">
              {{ successMessage }}
            </p>
            <div class="modal-actions">
              <button class="modal-btn success-btn" @click="showSuccessModal = false">
                <CheckCircle2 :size="18" />
                Continue
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script>
// Import API service for backend communication
import api from '@/services/api'

// Import Lucide icons for UI elements
import {
  Calculator,
  History as HistoryIcon,
  RefreshCw,
  Trash2,
  Copy,
  X,
  Equal,
  AlertTriangle,
  CheckCircle2,
  FileText  
} from 'lucide-vue-next'

export default {
  name: 'History',
  
  // Props received from parent component
  props: {
    isGuest: {
      type: Boolean,
      required: true
    }
  },
  
  components: {
    Calculator,
    History: HistoryIcon,
    RefreshCw,
    Trash2,
    Copy,
    X,
    Equal,
    AlertTriangle,
    CheckCircle2,
    FileText 
  },
  
  data() {
    return {
      history: [],              // Array to store calculation history
      loading: false,           // Loading state for API requests
      showClearModal: false,    // Toggle for clear all confirmation modal
      showDeleteModal: false,   // Toggle for delete item confirmation modal
      showSuccessModal: false,  // Toggle for success message modal
      successMessage: '',       // Dynamic success message text
      itemToDelete: null        // Stores ID of item to be deleted
    }
  },
  
  // Fetch history when component is mounted
  mounted() {
    this.fetchHistory()
  },
  
  methods: {
    /**
     * Fetches calculation history from backend
     * Handles errors gracefully and ensures history is always an array
     */
    async fetchHistory() {
      this.loading = true
      try {
        const res = await api.get('/history/')
        // Safety check: Ensure response is array to prevent errors
        this.history = Array.isArray(res.data) ? res.data : []
      } catch (err) {
        console.error('Failed to load history:', err)
        this.history = []
      } finally {
        this.loading = false
      }
    },

    /**
     * Formats operators to display mathematical symbols
     * Example: '*' becomes '×', '/' becomes '÷'
     */
    formatOperator(op) {
      const operators = {
        '*': '×',
        '/': '÷',
        '+': '+',
        '-': '−'
      }
      return operators[op] || op
    },

    /**
     * Formats numbers with proper locale formatting
     * Adds thousand separators and limits decimal places
     */
    formatNumber(value) {
      if (typeof value !== 'number') return value
      return new Intl.NumberFormat('en-US', {
        maximumFractionDigits: 10
      }).format(value)
    },

    /**
     * Copies result to clipboard using Clipboard API
     * Shows success modal on successful copy
     */
    async copyResult(result) {
      try {
        await navigator.clipboard.writeText(result.toString())
        this.successMessage = 'Result copied to clipboard!'
        this.showSuccessModal = true
      } catch (err) {
        console.error('Failed to copy:', err)
      }
    },

    /**
     * Shows confirmation modal before deleting an item
     * Stores the item ID for later use
     */
    confirmDelete(id) {
      this.itemToDelete = id
      this.showDeleteModal = true
    },

    /**
     * Deletes a single calculation item
     * Handles network errors (offline mode) gracefully
     * Updates UI optimistically for better UX
     */
    async deleteItem() {
      if (this.isGuest) {
        alert('Login required to delete items.')
        return
      }
      
      try {
        await api.delete(`/history/${this.itemToDelete}/`)
        
        // Remove item from local array
        this.history = this.history.filter(item => item.id !== this.itemToDelete)
        this.showDeleteModal = false
        this.itemToDelete = null
        
        this.successMessage = 'Calculation deleted successfully!'
        this.showSuccessModal = true
      } catch (err) {
        // Handle offline scenarios where network request fails
        if (err.code === 'ERR_NETWORK' || err.message === 'Network Error') {
          this.history = this.history.filter(item => item.id !== this.itemToDelete)
          this.showDeleteModal = false
          this.itemToDelete = null
          this.successMessage = 'Calculation deleted successfully!'
          this.showSuccessModal = true
        } else {
          console.error('Delete failed:', err)
          this.showDeleteModal = false
          // Show appropriate error based on status code
          if (err.response?.status === 401 || err.response?.status === 403) {
            alert('Login required to delete items.')
          } else {
            alert('Failed to delete calculation. Please try again.')
          }
        }
      }
    },

    /**
     * Shows confirmation modal before clearing all history
     */
    confirmClear() {
      if (this.isGuest) {
        alert('Login required to clear history.')
        return
      }
      this.showClearModal = true
    },

    /**
     * Clears all calculation history
     * Similar error handling as deleteItem
     */
    async clearAll() {
      if (this.isGuest) {
        alert('Login required to clear history.')
        return
      }
      
      try {
        await api.delete('/history/clear/')
        
        this.history = []
        this.showClearModal = false
        
        this.successMessage = 'All history cleared successfully!'
        this.showSuccessModal = true
      } catch (err) {
        // Handle network errors for offline functionality
        if (err.code === 'ERR_NETWORK' || err.message === 'Network Error') {
          this.history = []
          this.showClearModal = false
          this.successMessage = 'All history cleared successfully!'
          this.showSuccessModal = true
        } else {
          console.error('Clear failed:', err)
          this.showClearModal = false
          if (err.response?.status === 401 || err.response?.status === 403) {
            alert('Login required to clear history.')
          } else {
            alert('Failed to clear history. Please try again.')
          }
        }
      }
    }
  }
}
</script>

<style scoped>
/* Main wrapper for history component */
.history-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
}

/* Header section with count and action buttons */
.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.history-count {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

/* Large number display for total count */
.count-number {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--primary);
  line-height: 1;
}

.count-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

/* Action button styling with hover effects */
.action-button {
  width: 36px;
  height: 36px;
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

.action-button:hover:not(:disabled) {
  background: white;
  color: var(--text-primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Danger styling for clear button */
.action-button.clear {
  color: var(--danger);
}

.action-button.clear:hover {
  background: rgba(239, 68, 68, 0.08);
  border-color: rgba(239, 68, 68, 0.2);
}

/* Spinning animation for refresh button */
.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Loading state centered display */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: var(--text-secondary);
}

/* Spinner with rotating animation */
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(59, 130, 246, 0.1);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

/* Scrollable history list with custom scrollbar */
.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow-y: auto;
  max-height: 600px;
  padding-right: 0.5rem;
}

/* Custom scrollbar styling for better UX */
.history-list::-webkit-scrollbar {
  width: 6px;
}

.history-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.02);
  border-radius: 10px;
}

.history-list::-webkit-scrollbar-thumb {
  background: rgba(59, 130, 246, 0.2);
  border-radius: 10px;
}

.history-list::-webkit-scrollbar-thumb:hover {
  background: rgba(59, 130, 246, 0.3);
}

/* Individual history item with hover effects */
.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
}

/* Smooth slide-in effect on hover */
.history-item:hover {
  background: white;
  border-color: rgba(59, 130, 246, 0.15);
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.item-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  min-width: 0;
}

/* Icon container with gradient background */
.item-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  flex-shrink: 0;
}

.item-details {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex: 1;
  min-width: 0;
}

/* Expression display (operand operator operand) */
.expression {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  color: var(--text-primary);
}

.operand {
  font-weight: 600;
}

.operator {
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
}

/* Result line with equal sign */
.result-line {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  font-size: 0.85rem;
}

/* Emphasized result display */
.result {
  font-weight: 700;
  color: var(--primary);
  font-size: 1.1rem;
}

/* Note display with subtle background and border */
.note-display {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: rgba(59, 130, 246, 0.05);
  border-left: 2px solid rgba(59, 130, 246, 0.3);
  border-radius: 6px;
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
  line-height: 1.4;
}

.note-display svg {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--primary);
}

.note-display span {
  word-break: break-word;
}

/* Action buttons: Hidden by default, shown on hover */
.item-actions {
  display: flex;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.history-item:hover .item-actions {
  opacity: 1;
}

/* Individual action button styling */
.item-action-btn {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
}

.item-action-btn:hover {
  background: white;
  color: var(--text-primary);
}

/* Delete button with danger styling */
.item-action-btn.delete {
  color: var(--danger);
}

.item-action-btn.delete:hover {
  background: rgba(239, 68, 68, 0.08);
  border-color: rgba(239, 68, 68, 0.2);
}

/* Empty state display when no history exists */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.08));
  border: 1px solid rgba(59, 130, 246, 0.15);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  margin-bottom: 1.5rem;
}

.empty-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.empty-description {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Modal overlay with backdrop blur */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

/* Modal content card */
.modal-content {
  background: white;
  width: 90%;
  max-width: 420px;
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

/* Icon containers for modal (warning/success) */
.modal-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 1.5rem;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.modal-icon.warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.modal-icon.success {
  background: linear-gradient(135deg, #10b981, #059669);
}

.modal-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
}

.modal-description {
  text-align: center;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 2rem;
}

/* Modal action buttons container */
.modal-actions {
  display: flex;
  gap: 0.75rem;
}

/* Base modal button styling */
.modal-btn {
  flex: 1;
  padding: 0.9rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

/* Cancel button styling */
.modal-btn.cancel {
  background: rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(0, 0, 0, 0.1);
  color: var(--text-primary);
}

.modal-btn.cancel:hover {
  background: rgba(0, 0, 0, 0.08);
}

/* Confirm button with danger gradient */
.modal-btn.confirm {
  background: linear-gradient(135deg, var(--danger), #dc2626);
  border: none;
  color: white;
}

.modal-btn.confirm:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

/* Success button with success gradient */
.modal-btn.success-btn {
  width: 100%;
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  color: white;
}

.modal-btn.success-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

/* List transition animations for smooth item removal */
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.list-move {
  transition: transform 0.3s ease;
}

/* Modal transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9) translateY(20px);
}

/* Responsive design for mobile devices */
@media (max-width: 640px) {
  .history-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  /* Keep actions visible on mobile */
  .item-actions {
    opacity: 1;
    align-self: flex-end;
  }

  .expression {
    flex-wrap: wrap;
  }
}
</style>