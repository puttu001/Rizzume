"use client";

import Link from "next/link";
import { useState } from "react";

import { startInterview, type InterviewStartResponse } from "@/features/interview/api";
import { ApiError } from "@/lib/api-client";

export function InterviewSetupForm({
  onStarted,
}: {
  onStarted: (response: InterviewStartResponse) => void;
}) {
  const [roleTitle, setRoleTitle] = useState("");
  const [resume, setResume] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!resume) {
      setError("Upload your resume as a PDF.");
      return;
    }
    if (resume.type !== "application/pdf") {
      setError("Resume must be a PDF file.");
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await startInterview(resume, roleTitle);
      onStarted(response);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong. Try again.");
      setIsSubmitting(false);
    }
  }

  if (isSubmitting) {
    return (
      <div className="mx-auto flex w-full max-w-md flex-1 flex-col items-center justify-center px-6 py-16 text-center">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-indigo-200 border-t-indigo-600" />
        <p className="mt-6 font-medium text-slate-900">Setting up your interview…</p>
        <p className="mt-1 text-sm text-slate-500">
          Reading your resume and preparing questions — this can take up to 20 seconds.
        </p>
      </div>
    );
  }

  return (
    <div className="mx-auto flex w-full max-w-md flex-1 flex-col justify-center px-6 py-16">
      <Link href="/dashboard" className="mb-6 text-sm font-medium text-slate-500 hover:text-slate-900">
        ← Back to dashboard
      </Link>
      <h1 className="text-2xl font-bold text-slate-900">Start a new interview</h1>
      <p className="mt-1 text-sm text-slate-600">
        Upload your resume and tell us the role — the interviewer will ask
        questions grounded in your actual experience.
      </p>

      <form onSubmit={handleSubmit} className="mt-6 flex flex-col gap-4">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="roleTitle" className="text-sm font-medium text-slate-700">
            Role you&apos;re targeting
          </label>
          <input
            id="roleTitle"
            type="text"
            required
            value={roleTitle}
            onChange={(e) => setRoleTitle(e.target.value)}
            placeholder="e.g. Senior Backend Engineer"
            className="rounded-xl border border-slate-300 px-3.5 py-2.5 text-sm text-slate-900 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label htmlFor="resume" className="text-sm font-medium text-slate-700">
            Resume (PDF)
          </label>
          <input
            id="resume"
            type="file"
            accept="application/pdf"
            required
            onChange={(e) => setResume(e.target.files?.[0] ?? null)}
            className="rounded-xl border border-slate-300 px-3.5 py-2.5 text-sm text-slate-900 outline-none file:mr-3 file:rounded-full file:border-0 file:bg-indigo-50 file:px-3 file:py-1.5 file:text-sm file:font-medium file:text-indigo-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
          />
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          className="mt-2 rounded-full bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition-colors hover:bg-indigo-500"
        >
          Start Interview
        </button>
      </form>
    </div>
  );
}