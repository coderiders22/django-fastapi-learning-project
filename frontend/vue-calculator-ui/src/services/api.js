// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://calculatorpro-django-backend.koyeb.app/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch CSRF cookie once (Django requirement)
 */
export const initCSRF = async () => {
  try {
    await api.get('/auth/csrf/', { withCredentials: true });

  } catch (error) {

  }
};

/**
 * 🔐 Attach CSRF token automatically
 */
api.interceptors.request.use((config) => {
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];

  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }

  // 🔥 Ensure credentials are always sent
  config.withCredentials = true;

  return config;
});

/**
 * Response interceptor
 */
api.interceptors.response.use(
  (response) => {

    return response;
  },
  (error) => {


    if (error.response?.status === 401) {

      window.location.href = '/login?session_expired=true';
    }
    return Promise.reject(error);
  }
);

export default api;