/**
 * API Service layer for SCANNAI Forensic Engine.
 * Handles communication with FastAPI backend endpoints.
 * Product: SCANNAI | Team: ROCKERZ
 */

import { AnalysisResponse, HealthResponse, ApiError } from '../types/analysis';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

/**
 * Normalizes API endpoint URLs to support both relative proxying and direct host calls.
 */
function getEndpoint(path: string): string {
  if (BASE_URL) {
    // Ensure no double slashes
    return `${BASE_URL.replace(/\/$/, '')}${path}`;
  }
  return path;
}

/**
 * Checks system operational status and ingestion configuration.
 */
export async function fetchHealth(): Promise<HealthResponse> {
  const url = getEndpoint('/api/v1/health');
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Health check failed (${response.status}): ${errorText || response.statusText}`);
  }

  return response.json();
}

/**
 * Submits suspicious message text and/or evidence files to the deterministic forensic engine.
 */
export async function submitForAnalysis(
  messageText?: string,
  file?: File | null,
  caseReference?: string,
  ephemeralMode = false
): Promise<AnalysisResponse> {
  const url = getEndpoint('/api/v1/analyze');
  const formData = new FormData();

  if (messageText && messageText.trim()) {
    formData.append('message_text', messageText.trim());
  }

  if (file) {
    formData.append('file', file, file.name);
  }

  if (caseReference) {
    formData.append('case_reference', caseReference.trim());
  }

  formData.append('ephemeral_mode', String(ephemeralMode));

  const response = await fetch(url, {
    method: 'POST',
    body: formData,
    headers: {
      'Accept': 'application/json',
      // Note: Do NOT set Content-Type header when sending FormData!
      // The browser sets multipart/form-data with the correct boundary automatically.
    },
  });

  if (!response.ok) {
    let errorData: ApiError;
    try {
      errorData = await response.json();
    } catch {
      errorData = {
        message: `Analysis failed with HTTP ${response.status}: ${response.statusText}`,
      };
    }

    // Handle Pydantic validation error schema
    if (errorData.details && Array.isArray(errorData.details)) {
      const fieldErrors = errorData.details
        .map((d) => (d.field ? `${d.field}: ${d.message}` : d.message))
        .join('; ');
      throw new Error(`${errorData.message} (${fieldErrors})`);
    }

    // Handle standard FastAPI HTTPException { "detail": "..." } or structured security errors
    const rawDetail = (errorData as unknown as { detail?: unknown }).detail;
    if (rawDetail) {
      if (typeof rawDetail === 'string') {
        throw new Error(rawDetail);
      }
      if (typeof rawDetail === 'object' && rawDetail !== null) {
        const detailObj = rawDetail as { message?: string; error_code?: string; [key: string]: unknown };
        if (detailObj.message) {
          throw new Error(detailObj.message);
        }
        if (Array.isArray(rawDetail)) {
          const msgs = rawDetail
            .map((e: { msg?: string; message?: string }) => e.msg || e.message || JSON.stringify(e))
            .join('; ');
          throw new Error(msgs);
        }
      }
    }

    throw new Error(errorData.message || 'Analysis failed due to an unexpected error.');
  }

  return response.json();
}
