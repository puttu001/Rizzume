"use client";

import { createContext, useCallback, useContext, useEffect, useState } from "react";

import * as authApi from "@/features/auth/api";
import { tokenStorage } from "@/lib/token-storage";

interface AuthContextValue {
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // localStorage only exists client-side, so the real auth state can only
    // be known after mount — isLoading must stay true until then.
    //
    // This can't be a useSyncExternalStore with getServerSnapshot=false
    // instead: that makes ProtectedRoute's very first effect run (child
    // effects fire before ancestor effects, so it fires before this one
    // corrects the value) see a *determined* "not authenticated" state and
    // redirect to /signin before the correction lands — reproduced on a
    // hard reload of an authenticated /dashboard. isLoading gives
    // ProtectedRoute a genuine "not yet checked" state to gate on instead.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setIsAuthenticated(tokenStorage.getAccessToken() !== null);
    setIsLoading(false);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const tokens = await authApi.login(email, password);
    tokenStorage.setTokens(tokens.access_token, tokens.refresh_token);
    setIsAuthenticated(true);
  }, []);

  const signup = useCallback(async (email: string, password: string) => {
    const tokens = await authApi.signup(email, password);
    tokenStorage.setTokens(tokens.access_token, tokens.refresh_token);
    setIsAuthenticated(true);
  }, []);

  const logout = useCallback(() => {
    tokenStorage.clearTokens();
    setIsAuthenticated(false);
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}