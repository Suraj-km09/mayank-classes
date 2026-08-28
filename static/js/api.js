/**
 * API Client & Global Helpers for Mayank Classes Platform
 */

const API_BASE = '/api';

// Toast Notification Manager
function showToast(message, type = 'info', duration = 4000) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  let icon = 'ℹ️';
  if (type === 'success') icon = '✅';
  if (type === 'error') icon = '⚠️';
  if (type === 'warning') icon = '🔔';

  toast.innerHTML = `<span>${icon}</span><div>${message}</div>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Global API Request Wrapper
async function apiRequest(endpoint, method = 'GET', data = null, customHeaders = {}) {
  const token = localStorage.getItem('mc_auth_token');
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...customHeaders
  };

  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }

  const config = {
    method,
    headers
  };

  if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
    config.body = JSON.stringify(data);
  }

  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;

  try {
    const response = await fetch(url, config);
    
    // Handle 401 Unauthorized
    if (response.status === 401 && !endpoint.includes('auth/login')) {
      localStorage.removeItem('mc_auth_token');
      localStorage.removeItem('mc_user');
      // If currently in a portal, redirect to login
      if (window.location.pathname.includes('/student') || 
          window.location.pathname.includes('/teacher') || 
          window.location.pathname.includes('/admin-portal')) {
        window.location.href = '/login/?expired=true';
      }
    }

    const responseData = await response.json().catch(() => ({}));

    if (!response.ok) {
      const errorMsg = responseData.error || responseData.detail || responseData.message || (typeof responseData === 'object' ? Object.values(responseData).flat().join(', ') : 'Request failed');
      throw new Error(errorMsg || `HTTP Error ${response.status}`);
    }

    return responseData;
  } catch (error) {
    console.error(`API Error [${method} ${endpoint}]:`, error);
    throw error;
  }
}

// Utility Formatters
function formatCurrency(amount) {
  if (isNaN(amount)) return '₹0';
  return '₹' + Number(amount).toLocaleString('en-IN');
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

// Exported API helper
const api = {
  get: (endpoint) => apiRequest(endpoint, 'GET'),
  post: (endpoint, data) => apiRequest(endpoint, 'POST', data),
  put: (endpoint, data) => apiRequest(endpoint, 'PUT', data),
  patch: (endpoint, data) => apiRequest(endpoint, 'PATCH', data),
  delete: (endpoint) => apiRequest(endpoint, 'DELETE'),
};
