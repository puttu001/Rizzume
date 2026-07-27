"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { useAuth } from "@/features/auth/AuthProvider";

export function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const pathname = usePathname();

  // The interview session screen has its own self-contained top bar
  // (logo, timer, End Interview) — stacking the global nav above it would
  // duplicate the logo and give two different "exit" affordances.
  if (pathname?.startsWith("/interview")) {
    return null;
  }

  return (
    <header className="relative z-10 flex items-center justify-between px-6 py-5 sm:px-10">
      <Link href="/" className="flex items-center gap-2 text-lg font-semibold text-slate-900">
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-sm text-white">
          R
        </span>
        Rizzume
      </Link>

      {!isAuthenticated && (
        <nav className="hidden items-center gap-8 text-sm font-medium text-slate-600 sm:flex">
          <Link href="/#how-it-works" className="hover:text-slate-900">
            How it works
          </Link>
          <Link href="/#features" className="hover:text-slate-900">
            Features
          </Link>
        </nav>
      )}

      <div className="flex items-center gap-3">
        {isAuthenticated ? (
          <>
            <Link
              href="/dashboard"
              className="text-sm font-medium text-slate-700 hover:text-slate-900"
            >
              Dashboard
            </Link>
            <button
              onClick={logout}
              className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50"
            >
              Sign out
            </button>
          </>
        ) : (
          <>
            <Link
              href="/signin"
              className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50"
            >
              Sign in
            </Link>
            <Link
              href="/signup"
              className="rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-slate-800"
            >
              Sign up
            </Link>
          </>
        )}
      </div>
    </header>
  );
}