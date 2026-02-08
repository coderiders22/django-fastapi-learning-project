// Import axios for making HTTP requests
import axios from 'axios'

/**
 * Base API instance with axios
 * 
 * This is the main API client used throughout the app for all backend requests.
 * Uses environment variable for base URL so it works in both development and production.
 * 
 * withCredentials: true ensures cookies (session/CSRF) are sent with every request
 */
const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/api`,
  withCredentials: true,
})

/**
 * Initialize CSRF token
 * 
 * This function fetches the CSRF token from backend when the app starts.
 * The token is stored in a cookie and used to protect against CSRF attacks.
 * 
 * We call this in main.js before mounting the app to ensure the token
 * is ready before any POST/PUT/DELETE requests are made.
 * 
 * If it fails, we just log a warning - the app can still load,
 * but protected API calls might fail until token is fetched.
 */
export const initCSRF = async () => {
  try {
    await api.get('/auth/csrf/', {
      withCredentials: true,
    })
  } catch (error) {
    // Non-fatal error - app continues even if CSRF init fails
    console.warn('CSRF init failed (non-fatal):', error)
  }
}

/**
 * Request Interceptor
 * 
 * This runs before every API request and automatically adds the CSRF token
 * to the request headers. This saves us from manually adding it in every
 * POST/PUT/DELETE request.
 * 
 * How it works:
 * 1. Extract CSRF token from browser cookies
 * 2. Add it to X-CSRFToken header
 * 3. Ensure withCredentials is true (for session cookies)
 */
api.interceptors.request.use((config) => {
  // Parse CSRF token from cookies
  // Cookies are stored as "name=value; name2=value2" so we split and find csrftoken
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1]  // Optional chaining in case cookie doesn't exist

  // Add CSRF token to request headers if it exists
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken
  }

  // Ensure cookies are sent with request (important for session auth)
  config.withCredentials = true
  return config
})

/**
 * Response Interceptor
 * 
 * This runs after every API response and handles global errors.
 * 
 * Main purpose: Handle 401 Unauthorized errors globally
 * - If user's session expires or they're not authenticated
 * - Automatically redirect to login page
 * - Add query param to show "session expired" message
 **/
api.interceptors.response.use(
  // Success case - just return the response as-is
  (response) => response,

  // Error case - check if it's a 401 and redirect if needed
  (error) => {
    // If unauthorized (session expired or not logged in)
    if (error.response?.status === 401) {
      // Clear auth flag so router knows we are logged out
      localStorage.removeItem('is_authenticated')
      localStorage.removeItem('user')

      // Redirect to login page with session_expired flag
      window.location.href = '/login?session_expired=true'
    }

    // Reject the promise so the calling code can catch the error
    return Promise.reject(error)
  }
)

// Export the configured axios instance as default
export default api