// src/services/api.js
import axios from 'axios';

const isDev = process.env.NODE_ENV === 'development';
const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL?.trim();

if (!isDev && !backendUrl) {
  console.warn('NEXT_PUBLIC_BACKEND_URL is not set — running in demo mode (no backend calls).');
}

// Only create axios instance if we have a valid base URL
const api = (isDev || backendUrl)
  ? axios.create({
      baseURL: isDev ? '/specs' : `${backendUrl}/specs`,
      timeout: 60000,
    })
  : null;

export async function generateSpec(input) {
  // Early return with friendly error if no backend available
  if (!isDev && !backendUrl) {
    throw new Error(
      'Backend is not configured yet. This is a frontend demo — generation is disabled until the backend is deployed.'
    );
  }

  // Safe to call now — api is guaranteed to exist
  const response = await api.post('/generate', { input });
  return response.data;
}

export async function refineSpec(spec, refinementText, traceId) {
  if (!isDev && !backendUrl) {
    throw new Error(
      'Backend is not configured yet. Refinement is disabled in demo mode.'
    );
  }

  const response = await api.post('/refine', {
    spec,
    refinement_text: refinementText,
    trace_id: traceId,
  });
  return response.data;
}
