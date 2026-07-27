import { QuestionMarkIcon } from "@/features/interview/components/icons";

// Left column: the current question, prominent and always visible (not
// audio-only — matters for accessibility and re-reading long/technical
// questions), plus a stepped list of every question asked so far.
//
// The reference design this was built from showed fixed named stages
// ("Introduction", "System Design", ...) — the backend doesn't actually
// track named stages, only a running question count, so this uses the
// real question list instead of fabricating stage labels that don't
// correspond to anything real.
export function QuestionPanel({ questions }: { questions: string[] }) {
  const currentQuestion = questions[questions.length - 1];

  return (
    <div className="flex flex-col gap-6">
      <div className="rounded-2xl border border-slate-200 bg-white/80 p-6">
        <div className="flex items-center gap-2 text-sm font-semibold text-slate-900">
          <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
            <QuestionMarkIcon className="h-4 w-4" />
          </span>
          Interview Question
        </div>
        <div className="mt-3 h-1 w-full overflow-hidden rounded-full bg-slate-100">
          <div className="h-full w-1/3 rounded-full bg-indigo-600" />
        </div>
        <p className="mt-4 whitespace-pre-line text-sm leading-6 text-slate-700">
          {currentQuestion}
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white/80 p-6">
        <div className="flex items-center justify-between text-sm font-semibold text-slate-900">
          <span>Your Progress</span>
          <span className="font-normal text-slate-400">{questions.length} asked</span>
        </div>

        <ol className="mt-4 flex max-h-80 flex-col overflow-y-auto pr-1">
          {questions.map((question, index) => {
            const isCurrent = index === questions.length - 1;
            const isPast = index < questions.length - 1;
            const isLast = index === questions.length - 1;

            return (
              <li key={index} className="relative flex gap-3 pb-5 last:pb-0">
                {!isLast && (
                  <span className="absolute left-3 top-6 h-full w-px -translate-x-1/2 bg-slate-200" />
                )}
                <span
                  className={
                    "z-10 flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-semibold " +
                    (isCurrent
                      ? "bg-indigo-600 text-white"
                      : isPast
                        ? "bg-indigo-100 text-indigo-600"
                        : "bg-slate-100 text-slate-400")
                  }
                >
                  {index + 1}
                </span>
                <span
                  className={
                    "line-clamp-2 text-sm leading-6 " +
                    (isCurrent ? "font-medium text-slate-900" : "text-slate-500")
                  }
                >
                  {question}
                </span>
              </li>
            );
          })}
        </ol>
      </div>
    </div>
  );
}