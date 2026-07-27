// Self-contained visual mock of the actual interview screen (question list +
// speaking avatar indicator) — used on the landing hero instead of a stock
// photo so it doubles as a preview of the real product.
export function InterviewPreviewCard() {
  return (
    <div className="relative mx-auto w-full max-w-md rounded-3xl border border-slate-200 bg-white/80 p-6 shadow-2xl shadow-indigo-900/10 backdrop-blur">
      <div className="flex items-center gap-3 border-b border-slate-100 pb-4">
        <div className="relative flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-indigo-500 to-violet-600">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-indigo-400 opacity-40" />
          <span className="relative h-3 w-3 rounded-full bg-white" />
        </div>
        <div>
          <p className="text-sm font-semibold text-slate-900">Interviewer</p>
          <p className="text-xs font-medium text-emerald-600">Speaking…</p>
        </div>
      </div>

      <ul className="mt-4 space-y-3 text-sm">
        <li className="rounded-xl bg-slate-50 px-4 py-3 text-slate-700">
          Tell me about a time you debugged a production issue under pressure.
        </li>
        <li className="rounded-xl bg-slate-50 px-4 py-3 text-slate-500">
          Walk me through how you&apos;d design a rate limiter for a public API.
        </li>
        <li className="rounded-xl border border-dashed border-slate-200 px-4 py-3 text-slate-400">
          Next question appears here…
        </li>
      </ul>

      <div className="mt-5 flex items-center gap-2 rounded-xl bg-indigo-50 px-4 py-3 text-xs font-medium text-indigo-700">
        <span className="h-2 w-2 rounded-full bg-indigo-500" />
        Resume-aware · adapts difficulty as you answer
      </div>
    </div>
  );
}