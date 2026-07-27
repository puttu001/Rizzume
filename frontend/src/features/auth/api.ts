import { apiClient } from "@/lib/api-client";

// Mirrors auth-service's app/schemas/user.py — kept in sync by hand since
// each service is independent (no shared types package).
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  created_at: string;
}

export function signup(email: string, password: string): Promise<TokenResponse> {
  return apiClient.post<TokenResponse>("/api/v1/auth/signup", { email, password });
}

export function login(email: string, password: string): Promise<TokenResponse> {
  return apiClient.post<TokenResponse>("/api/v1/auth/login", { email, password });
}

export function refresh(refreshToken: string): Promise<TokenResponse> {
  return apiClient.post<TokenResponse>("/api/v1/auth/refresh", {
    refresh_token: refreshToken,
  });
}

export function getMe(): Promise<User> {
  return apiClient.get<User>("/api/v1/auth/me");
}