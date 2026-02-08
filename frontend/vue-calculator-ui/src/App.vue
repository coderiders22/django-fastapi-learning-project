<!-- src/App.vue -->
<template>
  <div id="app">
    <!-- Navbar component will be visible on all pages -->
    <Navbar />
    
    <!-- Router view renders the current route's component -->
    <router-view />
  </div>
</template>

<script>
// Import the Navbar component to use across all pages
import Navbar from './components/Navbar.vue'

export default {
  // Register Navbar as a component
  components: {
    Navbar
  }
}
</script>