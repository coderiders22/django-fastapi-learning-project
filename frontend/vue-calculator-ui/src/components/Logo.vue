<!-- src/components/Logo.vue -->
<!-- 
  Brand Logo Component
  - Displays "CalcPro" text using SVG for crisp rendering
  - Supports small variant via prop
  - Uses gradient colors matching brand theme
-->
<template>
  <!-- Wrapper with conditional small class for size variation -->
  <div class="logo-wrapper" :class="{ small: small }">
    <!-- SVG element for text logo - better quality than regular text -->
    <svg viewBox="0 0 380 100" class="logo-svg">
      <!-- "Calc" text - uses primary text color from CSS variables -->
      <text x="0" y="72" class="text-calc">Calc</text>
      <!-- "Pro" text - uses brand primary color for emphasis -->
      <text x="172" y="72" class="text-pro">Pro</text>
    </svg>
  </div>
</template>

<script>
export default {
  // Accepts optional small prop to render smaller version
  props: { small: Boolean }
}
</script>

<style scoped>
/* Container for logo - inline-flex to fit content width */
.logo-wrapper {
  display: inline-flex;
  align-items: center;
}

/* SVG sizing - maintains aspect ratio automatically */
.logo-svg {
  height: 42px;
  width: auto;  /* Width adjusts automatically based on viewBox */
}

/* "Calc" text styling */
.text-calc {
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 800;  /* Extra bold */
  font-size: 68px;
  fill: var(--text-primary);  /* Uses CSS variable for theming */
  letter-spacing: -0.04em;  /* Negative spacing for tighter, modern look */
}

/* "Pro" text styling - matches Calc but with brand color */
.text-pro {
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 900;  /* Black weight for emphasis */
  font-size: 68px;
  fill: var(--primary);  /* Brand primary blue color */
  letter-spacing: -0.03em;
}

/* Small variant sizing for compact layouts */
.small .logo-svg {
  height: 32px;
}

/* Reduces font size proportionally in small variant */
.small .text-calc,
.small .text-pro {
  font-size: 52px;
}
</style>