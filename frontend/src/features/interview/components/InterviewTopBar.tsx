import Link from "next/link";

import { ClockIcon, ListIcon, PowerIcon } from "@/features/interview/components/icons";

export function InterviewTopBar({
  elapsedLabel,
  questionNumber,
  maxQuestions,
  onEndInterview,
}: {
  elapsedLabel: string;
  questionNumber: number;
  maxQuestions: number;
  onEndInterview: () => void;
}) {
  const progressPct = Math.min(100, Math.round((questionNumber / maxQuestions) * 100));

  return (
    <header className="flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-white/80 px-6 py-4">
      <Link href="/" className="flex items-center gap-2 text-lg font-semibold text-slate-900">
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-sm text-white">
          R
        </span>
        Rizzume
      </Link>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
            <ClockIcon />
          </span>
          <div>
            <p className="text-sm font-semibold text-slate-900">{elapsedLabel}</p>
            <p className="text-xs text-slate-500">Time Elapsed</p>
          </div>
        </div>

        <div className="hidden h-8 w-px bg-slate-200 sm:block" />

        <div className="flex items-center gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
            <ListIcon />
          </span>
          <div>
            <p className="text-sm font-semibold text-slate-900">
              Question {questionNumber} / {maxQuestions}
            </p>
            <p className="text-xs text-slate-500">Interview Progress</p>
            <div className="mt-1 h-1.5 w-32 overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-indigo-600 transition-all"
                style={{ width: `${progressPct}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      <button
        onClick={onEndInterview}
        className="flex items-center gap-2 rounded-full border border-red-200 px-4 py-2 text-sm font-semibold text-red-600 transition-colors hover:bg-red-50"
      >
        <PowerIcon />
        End Interview
      </button>
    </header>
  );
}