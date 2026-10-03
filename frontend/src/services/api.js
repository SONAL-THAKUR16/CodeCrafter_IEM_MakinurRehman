import axios from 'axios';

// Base API configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Helper for human-readable error formatting
const formatError = (error) => {
  if (error.response) {
    const detail = error.response.data?.detail || error.response.data?.error || 'Server error occurred.';
    if (typeof detail === 'string') return detail;
    if (Array.isArray(detail)) return detail.join(', ');
    if (typeof detail === 'object') return detail.message || JSON.stringify(detail);
  } else if (error.request) {
    return 'Unable to reach backend server. Please verify backend is running on http://localhost:8000.';
  }
  return error.message || 'An unexpected error occurred.';
};

export const api = {
  /** Health check endpoint */
  healthCheck: async () => {
    try {
      const res = await apiClient.get('/api/health');
      return { success: true, data: res.data };
    } catch (err) {
      return { success: false, error: formatError(err) };
    }
  },

  /** Analyze student academic feedback text */
  analyzeText: async (text) => {
    try {
      const res = await apiClient.post('/api/analyze', { text });
      return { success: true, data: res.data };
    } catch (err) {
      return { success: false, error: formatError(err) };
    }
  },

  /** Retrieve an individual analysis by ID */
  getAnalysis: async (analysisId) => {
    try {
      const res = await apiClient.get(`/api/analyze/${analysisId}`);
      return { success: true, data: res.data };
    } catch (err) {
      return { success: false, error: formatError(err) };
    }
  },

  /** Retrieve recent analysis history */
  getHistory: async (limit = 20) => {
    try {
      const res = await apiClient.get(`/api/history?limit=${limit}`);
      return { success: true, data: res.data };
    } catch (err) {
      return { success: false, error: formatError(err) };
    }
  },

  /** Retrieve real-time dashboard summary statistics */
  getDashboardSummary: async () => {
    try {
      const res = await apiClient.get('/api/dashboard/summary');
      return { success: true, data: res.data };
    } catch (err) {
      return { success: false, error: formatError(err) };
    }
  },

  /** Retrieve time-series trend data for charts */
  getDashboardTrends: async (limit = 20) => {
    try {
      const res = await apiClient.get(`/api/dashboard/trends?limit=${limit}`);
      return { success: true, data: res.data };
    } catch (err) {
      return { success: false, error: formatError(err) };
    }
  },
};

export default api;
