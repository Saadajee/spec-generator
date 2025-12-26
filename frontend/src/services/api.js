// src/services/api.js
import axios from 'axios';

// Create Axios instance (proxied in Vite to backend)
const api = axios.create({
  baseURL: '/specs', // Proxied to http://localhost:8000/specs via vite.config.js
  headers: {
    'Content-Type': 'application/json',
  },
});
// Extract meaningful error message from Axios error object
const extractErrorMessage = (error) => {
  if (!error.response) {
    return error.message || 'Network error — please check if the backend is running';
  }

  const data = error.response.data;

  // Case 1: FastAPI validation error → array of objects
  if (Array.isArray(data.detail)) {
    const messages = data.detail
      .map((item) => item.msg || item.message || 'Validation error')
      .filter(Boolean);
    return messages.length > 0 ? messages.join(' | ') : 'Invalid request format';
  }

  // Case 2: Simple string detail (e.g. custom HTTPException)
  if (typeof data.detail === 'string') {
    return data.detail;
  }

  // Case 3: Other common patterns
  if (data.message) return data.message;
  if (data.error) return data.error;

  // Fallback
  return `Server error: ${error.response.status}`;
};

// Generate a new spec from requirements
export const generateSpec = async (requirementsText) => {
  try {
    const response = await api.post('/generate', {
      requirements_text: requirementsText.trim(),
    });
    return response.data; // Expected: { trace_id: string, spec: object }
  } catch (error) {
    const message = extractErrorMessage(error);
    // Re-throw with clean message so caller can handle it
    error.message = message;
    throw error;
  }
};

// Refine an existing spec — REQUIRES trace_id for versioning
export const refineSpec = async (currentSpec, refinementText, traceId) => {
  if (!traceId) {
    throw new Error('traceId is required for refinement to maintain version history');
  }

  try {
    const response = await api.post('/refine', {
      current_spec: currentSpec,
      refinement_text: refinementText.trim(),
      trace_id: traceId, // Must be the original base trace_id
    });
    return response.data; // Expected: { trace_id: same, spec: refined }
  } catch (error) {
    const message = extractErrorMessage(error);
    error.message = message;
    throw error;
  }
};