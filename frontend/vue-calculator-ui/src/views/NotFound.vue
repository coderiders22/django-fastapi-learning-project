<!-- src/views/NotFound.vue -->
<template>
  <div class="not-found-page">
    <Navbar />

    <div class="not-found-content">
      <div class="error-container">
        <h1 class="error-code">404</h1>
        <h2 class="error-title">Page Not Found</h2>
        <p class="error-description">
          Oops! The page you're looking for doesn't seem to exist.<br />
          It might have been moved, deleted, or maybe you typed the wrong URL.
        </p>

        <div class="error-actions">
          <button class="btn btn-primary" @click="$router.push('/')">
            <span>Go to Home</span>
            <ArrowRight :size="18" />
          </button>
          <button class="btn btn-secondary" @click="$router.back()">
            Go Back
          </button>
        </div>
      </div>

      <!-- Optional fun element -->
      <div class="error-visual">
        <div class="calculator-ghost">
          <Calculator :size="120" />
          <span class="ghost-text">?</span>
        </div>
      </div>
    </div>

    <!-- Common Footer -->
    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { ArrowRight, Calculator } from 'lucide-vue-next'

export default {
  name: 'NotFound',
  components: {
    Navbar,
    Footer,
    ArrowRight,
    Calculator
  }
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.not-found-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  position: relative;
}

.error-container {
  text-align: center;
  max-width: 600px;
  z-index: 2;
}

.error-code {
  font-size: clamp(6rem, 20vw, 12rem);
  font-weight: 900;
  margin: 0;
  line-height: 0.9;
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.05em;
}

.error-title {
  font-size: clamp(2rem, 6vw, 3.5rem);
  font-weight: 800;
  color: var(--text-primary);
  margin: 1rem 0 1.5rem;
}

.error-description {
  font-size: 1.25rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.35);
}

.btn-secondary {
  background: white;
  color: var(--text-primary);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover {
  background: #f8fafc;
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

/* Visual fun element */
.error-visual {
  position: absolute;
  bottom: 10%;
  right: 5%;
  opacity: 0.15;
  pointer-events: none;
}

.calculator-ghost {
  position: relative;
}

.ghost-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 5rem;
  font-weight: 900;
  color: var(--primary);
  opacity: 0.4;
}

/* Responsive */
@media (max-width: 1024px) {
  .error-visual {
    display: none;
  }
}

@media (max-width: 768px) {
  .error-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>