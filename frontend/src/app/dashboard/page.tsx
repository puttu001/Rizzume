"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import * as authApi from "@/features/auth/api";

function DashboardContent() {
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    authApi
      .getMe()
      .then((user) => setEmail(user.email))
      .catch(() => setEmail(null));
  }, []);

  return (
    <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col items-center justify-center px-6 py-16 text-center">
      <p className="text-sm font-medium text-slate-500">
        {email ? `Welcome back, ${email}` : "Welcome back"}
      </p>
      <h1 className="mt-2 text-3xl font-bold text-slate-900">
        Ready to practice?
      </h1>
      <p className="mt-2 max-w-md text-slate-600">
        Upload your resume, pick a role, and start a real spoken interview.
      </p>

      <Link
        href="/interview/new"
        className="mt-8 rounded-full bg-indigo-600 px-8 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition-colors hover:bg-indigo-500"
      >
        Start New Interview
      </Link>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}