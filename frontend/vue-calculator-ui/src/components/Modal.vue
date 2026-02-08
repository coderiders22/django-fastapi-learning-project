<!-- src/components/Modal.vue -->
<!-- 
  Reusable Modal Component
  - Displays success, error, or warning messages
  - Uses dynamic icons and styling based on modal type
  - Click outside to close functionality
-->
<template>
  <!-- Overlay: darkens background and centers modal -->
  <div class="modal-overlay" @click.self="$emit('close')">
    <!-- Main modal card: stops propagation so clicking inside doesn't close -->
    <div class="modal-card" @click.stop>
      
      <!-- Icon Section: dynamically renders icon based on type prop -->
      <div class="modal-icon-wrapper" :class="type">
        <component :is="iconComponent" :size="40" />
      </div>

      <!-- Title: changes based on modal type (Success/Error/Warning) -->
      <h3 class="modal-title">
        {{ titleText }}
      </h3>
      
      <!-- Message text passed from parent component -->
      <p class="modal-text">{{ text }}</p>

      <!-- Action button: emits close event when clicked -->
      <button class="modal-action-btn" @click="$emit('close')">
        {{ buttonText }}
        <!-- Arrow icon only shows for success type -->
        <ArrowRight v-if="type === 'success'" :size="18" />
      </button>
    </div>
  </div>
</template>

<script>
// Importing icons from lucide-vue-next library
import { CheckCircle, AlertTriangle, ArrowRight, ShieldAlert } from 'lucide-vue-next'

export default {
  name: 'Modal',
  
  // Props received from parent component
  props: {
    text: {
      type: String,
      required: true  // Modal message is mandatory
    },
    type: {
      type: String,
      default: 'error',  // Defaults to error if not specified
      validator: value => ['error', 'success', 'warning'].includes(value)  // Only allows these 3 types
    }
  },
  
  // Registering icon components
  components: {
    CheckCircle,
    AlertTriangle,
    ArrowRight,
    ShieldAlert
  },
  
  computed: {
    // Dynamically selects which icon to show based on type
    iconComponent() {
      if (this.type === 'success') return 'CheckCircle'
      if (this.type === 'warning') return 'ShieldAlert'
      return 'AlertTriangle'  // Default for error
    },
    
    // Sets appropriate title text for each modal type
    titleText() {
      if (this.type === 'success') return 'Success!'
      if (this.type === 'warning') return 'Oops!'
      return 'Error!'
    },
    
    // Changes button text based on modal type
    buttonText() {
      if (this.type === 'success') return 'Continue'
      if (this.type === 'warning') return 'Try Again'
      return 'Close'
    }
  }
}
</script>

<style scoped>
/* Fullscreen overlay with blur effect */
.modal-overlay {
  position: fixed;
  inset: 0;  /* Shorthand for top:0, right:0, bottom:0, left:0 */
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(8px);  /* Creates frosted glass effect */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;  /* High z-index to appear above everything */
  animation: fadeIn 0.3s ease-out;
}

/* Main modal container */
.modal-card {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 420px;
  padding: 2.5rem 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);  /* Deep shadow for elevation */
  text-align: center;
  position: relative;
  overflow: hidden;
  animation: modalPop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);  /* Bouncy entrance animation */
}

/* Icon wrapper - circular background with gradient */
.modal-icon-wrapper {
  width: 90px;
  height: 90px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;  /* Makes it circular */
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

/* Success state: green gradient */
.modal-icon-wrapper.success {
  background: linear-gradient(135deg, #10b981, #059669);
}

/* Error state: red gradient */
.modal-icon-wrapper.error {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

/* Warning state: orange gradient */
.modal-icon-wrapper.warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

/* Modal title styling */
.modal-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 0.75rem;
  letter-spacing: -0.02em;  /* Tighter letter spacing for modern look */
}

/* Modal message text */
.modal-text {
  font-size: 1.1rem;
  color: #64748b;
  line-height: 1.6;  /* Better readability */
  margin-bottom: 2rem;
}

/* Primary action button */
.modal-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1rem 2.2rem;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

/* Hover effect: lifts button up */
.modal-action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.45);
}

/* Fade in animation for overlay */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Pop-up animation for modal card - scales and slides up */
@keyframes modalPop {
  from {
    opacity: 0;
    transform: scale(0.85) translateY(40px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Mobile responsive adjustments */
@media (max-width: 480px) {
  .modal-card {
    padding: 2rem 1.5rem;
  }
  .modal-title {
    font-size: 1.6rem;
  }
  .modal-text {
    font-size: 1rem;
  }
}
</style>