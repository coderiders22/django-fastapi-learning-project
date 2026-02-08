<!-- 
  Footer Component
  Displays app branding, developer credits, social links, and project info
  Uses glassmorphism design with gradient backgrounds
-->
<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- 
        Main Footer Content
        Two-column layout: Brand info on left, Credits on right
        Responsive: stacks to single column on mobile
      -->
      <div class="footer-content">
        
        <!-- Left Column: Brand and Tagline -->
        <div class="footer-brand">
          <div class="footer-logo">
            <!-- Logo icon with gradient background -->
            <div class="footer-logo-icon">
              <Calculator :size="24" />
            </div>
            <span class="footer-logo-text">CalculatorPro</span>
          </div>
          <!-- Brief description of the project -->
          <p class="footer-tagline">
            Django-based calculator with authentication, guest sessions, REST APIs, and admin dashboard.
          </p>
        </div>

        <!-- Right Column: Developer Credits and Social Links -->
        <div class="footer-credits">
          <p class="designed-by">
            Designed & Developed by <span class="developer-name">Manav Rai</span>
          </p>
          
          <!-- Social Media Links -->
          <div class="footer-social">
            <!-- Portfolio Link -->
            <a
              href="https://manavrai.netlify.app/"
              class="social-link"
              aria-label="Portfolio"
              target="_blank"
              rel="noopener noreferrer"
            >
              <User :size="20" />
            </a>

            <!-- LinkedIn Link -->
            <a
              href="https://www.linkedin.com/in/manavrai/"
              class="social-link"
              aria-label="LinkedIn"
              target="_blank"
              rel="noopener noreferrer"
            >
              <!-- Custom LinkedIn SVG icon -->
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"></path>
                <circle cx="4" cy="4" r="2"></circle>
              </svg>
            </a>

            <!-- GitHub Link -->
            <a
              href="https://github.com/coderiders22"
              class="social-link"
              aria-label="GitHub"
              target="_blank"
              rel="noopener noreferrer"
            >
              <!-- Custom GitHub SVG icon -->
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0020 4.77 5.07 5.07 0 0019.91 1S18.73.65 16 2.48a13.38 13.38 0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 005 4.77a5.44 5.44 0 00-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 009 18.13V22"
                ></path>
              </svg>
            </a>
          </div>
        </div>
      </div>

      <!-- 
        Footer Bottom Section
        Copyright and technology badges
      -->
      <div class="footer-bottom">
        <p class="footer-copyright">
          © 2026 CalculatorPro — Professional Calculator Application
        </p>
        
        <!-- Technology badges showing key features -->
        <div class="footer-badges">
          <span class="footer-badge">
            <Shield :size="14" />
            <span>Django Framework</span>
          </span>
          <span class="footer-badge">
            <Shield :size="14" />
            <span>Secure Sessions</span>
          </span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
// Import Lucide icons for footer elements
import { Calculator, Shield, User } from 'lucide-vue-next'

export default {
  name: 'AppFooter',
  components: {
    Calculator,
    Shield,
    User
  }
}
</script>

<style scoped>
/* ==================== Main Footer Container ==================== */
/* 
  Dark gradient background with subtle pattern overlay
  Creates professional, modern appearance
*/
.footer {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: white;
  padding: 4rem 5vw 2rem;
  position: relative;
  overflow: hidden;
}

/* 
  Decorative pattern overlay using SVG
  Adds texture without overwhelming the content
  Very subtle opacity (0.02) for background effect
*/
.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.4;
  pointer-events: none;
}

/* Center content with max width for readability */
.footer-container {
  max-width: 1320px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* ==================== Footer Content Layout ==================== */
/* 
  Grid layout for main content
  1.5fr for brand, 1fr for credits
  Creates visual hierarchy with more space for brand info
*/
.footer-content {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 4rem;
  margin-bottom: 3rem;
  padding-bottom: 3rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* ==================== Brand Section ==================== */
.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Logo with icon and text */
.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* 
  Logo icon with gradient and shadow
  Matches primary blue theme from calculator
*/
.footer-logo-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
}

/* 
  Logo text with gradient effect
  Uses webkit text-fill for gradient text
*/
.footer-logo-text {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(90deg, #ffffff, rgba(255, 255, 255, 0.8));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Project description tagline */
.footer-tagline {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  max-width: 500px;
  font-size: 0.95rem;
}

/* ==================== Credits and Social Section ==================== */
.footer-credits {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: flex-end;
}

.designed-by {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  text-align: right;
}

/* 
  Developer name with gradient effect
  Blue to pink gradient for visual interest
*/
.developer-name {
  color: white;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6, #ec4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ==================== Social Links ==================== */
/* Horizontal flex layout for social icons */
.footer-social {
  display: flex;
  gap: 0.75rem;
}

/* 
  Individual social link styling
  Glassmorphism effect with semi-transparent background
*/
.social-link {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
}

/* Hover effect: brighten and lift */
.social-link:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.2);
  color: white;
  transform: translateY(-2px);
}

/* ==================== Footer Bottom Section ==================== */
/* 
  Flex layout for copyright and badges
  Space between for balanced distribution
*/
.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.footer-copyright {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

/* ==================== Technology Badges ==================== */
.footer-badges {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

/* 
  Individual badge styling
  Pill-shaped with icon and text
  Shows technologies used in the project
*/
.footer-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.85rem;
  font-weight: 500;
}

/* ==================== Responsive Design ==================== */
/* 
  Tablet and below: Stack content vertically
  Change alignment from right to left for credits
*/
@media (max-width: 1024px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .footer-credits {
    align-items: flex-start;
    text-align: left;
  }

  .designed-by {
    text-align: left;
  }
}

/* 
  Mobile: Further simplifications
  Center align bottom content
*/
@media (max-width: 768px) {
  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }
}
</style>