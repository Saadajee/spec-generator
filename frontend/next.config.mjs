// src/services/api.js
import axios from 'axios';

const isDev = process.env.NODE_ENV === 'development';
const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

if (!isDev && !backendUrl) {
  console.warn('NEXT_PUBLIC_BACKEND_URL is not set — running in demo mode (no backend calls).');
}

const api = axios.create({
  baseURL: isDev ? '/specs' : backendUrl ? `${backendUrl}/specs` : null,
  timeout: 60000, // 60s timeout
});

export async function generateSpec(input) {
  if (!isDev && !backendUrl) {
    throw new Error(
      'Backend is not configured yet. This is a frontend demo — generation is disabled until the backend is deployed.'
    );
  }

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
