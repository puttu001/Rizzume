import { env } from "@/config/env";
import { tokenStorage } from "@/lib/token-storage";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

// FastAPI error responses are {"detail": "..."} — surface that string
// directly instead of the raw JSON blob when we can.
async function parseErrorMessage(response: Response): Promise<string> {
  try {
    const data = await response.json();
    if (typeof data?.detail === "string") return data.detail;
    return JSON.stringify(data);
  } catch {
    return response.statusText;
  }
}

function authHeaders(): Record<string, string> {
  const accessToken = tokenStorage.getAccessToken();
  return accessToken ? { Authorization: `Bearer ${accessToken}` } : {};
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${env.NEXT_PUBLIC_API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...init?.headers,
    },
  });

  if (!response.ok) {
    throw new ApiError(response.status, await parseErrorMessage(response));
  }

  if (response.status === 204) return undefined as T;

  return response.json() as Promise<T>;
}

// Multipart uploads (resume PDF, recorded audio) — no Content-Type header
// here on purpose: the browser sets multipart/form-data with the correct
// boundary itself, and overriding it manually breaks parsing.
async function requestFormData<T>(path: string, formData: FormData): Promise<T> {
  const response = await fetch(`${env.NEXT_PUBLIC_API_URL}${path}`, {
    method: "POST",
    headers: authHeaders(),
    body: formData,
  });

  if (!response.ok) {
    throw new ApiError(response.status, await parseErrorMessage(response));
  }

  return response.json() as Promise<T>;
}

// audio-service's /speech returns raw audio/mpeg bytes, not JSON.
async function requestBlob(path: string, body: unknown): Promise<Blob> {
  const response = await fetch(`${env.NEXT_PUBLIC_API_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new ApiError(response.status, await parseErrorMessage(response));
  }

  return response.blob();
}

// Talks to api-gateway only — this is the single point where the frontend
// crosses the network boundary into the backend.
export const apiClient = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: "POST", body: body !== undefined ? JSON.stringify(body) : undefined }),
  postFormData: <T>(path: string, formData: FormData) => requestFormData<T>(path, formData),
  postForBlob: (path: string, body: unknown) => requestBlob(path, body),
};