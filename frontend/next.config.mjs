// src/services/api.js
import axios from 'axios';

const isDev = process.env.NODE_ENV === 'development';
const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL?.trim();

if (!isDev && !backendUrl) {
  console.warn('NEXT_PUBLIC_BACKEND_URL is not set — running in demo mode (no backend calls).');
}

let api = null;
if (isDev || backendUrl) {
  api = axios.create({
    baseURL: isDev ? '/specs' : `${backendUrl}/specs`,
    timeout: 60000,
  });
}

export const generateSpec = async (input) => {
  if (!isDev && !backendUrl) {
    throw new Error(
      'Backend is not configured yet. This is a frontend demo — generation is disabled until the backend is deployed.'
    );
  }

  // FIXED: Use the exact field name your backend expects
  const response = await api.post('/generate', {
    requirements_text: input.trim(),
  });

  return response.data;
};

export const refineSpec = async (spec, refinementText, traceId) => {
  if (!isDev && !backendUrl) {
    throw new Error(
      'Backend is not configured yet. Refinement is disabled in demo mode.'
    );
  }

  // FIXED: Match backend model exactly
  const response = await api.post('/refine', {
    current_spec: spec,
    refinement_text: refinementText.trim(),
    trace_id: traceId,
  });

  return response.data;
};
