// Shared decorative background for the marketing/auth surface — rendered
// once in the root layout so landing → signup/signin navigation reads as
// one continuous canvas instead of a page swap.
export function BackgroundCanvas() {
  return (
    <div aria-hidden className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="absolute -top-32 -right-24 h-96 w-96 rounded-full bg-indigo-300/40 blur-3xl dark:bg-indigo-500/20" />
      <div className="absolute top-1/3 -left-32 h-80 w-80 rounded-full bg-emerald-300/30 blur-3xl dark:bg-emerald-500/10" />
      <div className="absolute bottom-0 right-1/4 h-72 w-72 rounded-full bg-sky-300/30 blur-3xl dark:bg-sky-500/10" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,#94a3b8_1px,transparent_0)] bg-[size:32px_32px] opacity-[0.15] dark:opacity-[0.07]" />
    </div>
  );
}