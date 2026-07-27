// MVP choice: localStorage for both tokens (not httpOnly cookies) — zero
// backend changes needed since api-gateway already expects a plain
// `Authorization: Bearer` header. Revisit if this app ever handles
// higher-stakes data than interview practice sessions.
const ACCESS_TOKEN_KEY = "rizzume_access_token";
const REFRESH_TOKEN_KEY = "rizzume_refresh_token";

function isBrowser(): boolean {
  return typeof window !== "undefined";
}

export const tokenStorage = {
  getAccessToken(): string | null {
    return isBrowser() ? localStorage.getItem(ACCESS_TOKEN_KEY) : null;
  },
  getRefreshToken(): string | null {
    return isBrowser() ? localStorage.getItem(REFRESH_TOKEN_KEY) : null;
  },
  setTokens(accessToken: string, refreshToken: string): void {
    if (!isBrowser()) return;
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  },
  clearTokens(): void {
    if (!isBrowser()) return;
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  },
};