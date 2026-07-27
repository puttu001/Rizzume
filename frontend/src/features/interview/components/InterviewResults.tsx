import Link from "next/link";

import type { Feedback } from "@/features/interview/api";

// report-service's polished PDF isn't part of the MVP results screen —
// this shows interview-service's raw feedback JSON directly instead.
export function InterviewResults({ feedback }: { feedback: Feedback }) {
  return (
    <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col justify-center px-6 py-16">
      <div className="rounded-3xl border border-slate-200 bg-white/90 p-8 shadow-2xl shadow-indigo-900/10 backdrop-blur">
        <p className="text-sm font-medium text-slate-500">Interview complete</p>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-5xl font-bold text-indigo-600">{feedback.overall_score}</span>
          <span className="text-lg text-slate-400">/ 100</span>
        </div>

        <p className="mt-4 leading-7 text-slate-700">{feedback.summary}</p>

        <div className="mt-6 grid gap-6 sm:grid-cols-2">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-emerald-600">
              Strengths
            </p>
            <ul className="mt-2 flex flex-col gap-2">
              {feedback.strengths.map((item, index) => (
                <li key={index} className="rounded-xl bg-emerald-50 px-3 py-2 text-sm text-emerald-900">
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-amber-600">
              Areas to improve
            </p>
            <ul className="mt-2 flex flex-col gap-2">
              {feedback.areas_for_improvement.map((item, index) => (
                <li key={index} className="rounded-xl bg-amber-50 px-3 py-2 text-sm text-amber-900">
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-8 flex justify-center gap-3">
          <Link
            href="/interview/new"
            className="rounded-full bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition-colors hover:bg-indigo-500"
          >
            Practice again
          </Link>
          <Link
            href="/dashboard"
            className="rounded-full border border-slate-300 px-6 py-2.5 text-sm font-semibold text-slate-700 transition-colors hover:bg-white"
          >
            Back to dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}