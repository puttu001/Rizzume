import { BrainIcon, ShieldIcon, SparkleIcon, BulbIcon } from "@/features/interview/components/icons";

const TIPS = [
  "Structure your answers using the STAR method: Situation, Task, Action, Result.",
  "It's okay to pause and think before answering — quality over speed.",
  "Be specific: name real projects, numbers, and outcomes where you can.",
  "If you don't know something, say so and explain how you'd find out.",
];

// Center column: the avatar (a stylized CSS/SVG orb, not a photorealistic
// character — no image-generation tool available for that), a waveform
// synced to real TTS playback, and static framing copy/trust badges. The
// live question text itself lives in QuestionPanel; this is deliberately
// not a duplicate of it.
export function AvatarPanel({
  isSpeaking,
  isRecording,
  questionIndex,
}: {
  isSpeaking: boolean;
  isRecording: boolean;
  questionIndex: number;
}) {
  const tip = TIPS[questionIndex % TIPS.length];
  const statusText = isSpeaking
    ? "Speaking the question…"
    : isRecording
      ? "I'm listening…"
      : "Take your time and share your thoughts.";

  return (
    <div className="flex flex-col items-center gap-6 rounded-2xl border border-slate-200 bg-white/80 p-8 text-center">
      <div className="flex items-center gap-4">
        <Waveform active={isSpeaking} />
        <AvatarOrb isSpeaking={isSpeaking} />
        <Waveform active={isSpeaking} />
      </div>

      <span className="inline-flex items-center gap-1.5 rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700">
        <SparkleIcon className="h-3.5 w-3.5" />
        AI Interviewer
      </span>

      <div>
        <h2 className="text-lg font-bold text-slate-900">Hello! I&apos;m your AI interviewer.</h2>
        <p className="mt-1 text-sm text-slate-500">{statusText}</p>
      </div>

      <div className="grid w-full grid-cols-1 gap-2 sm:grid-cols-3">
        <Badge icon={<BrainIcon className="h-3.5 w-3.5" />} label="Adaptive Follow-ups" />
        <Badge icon={<ShieldIcon className="h-3.5 w-3.5" />} label="Secure & Private" />
        <Badge icon={<SparkleIcon className="h-3.5 w-3.5" />} label="Real-time Evaluation" />
      </div>

      <div className="w-full rounded-xl bg-indigo-50/60 p-4 text-left">
        <p className="flex items-center gap-2 text-xs font-semibold text-indigo-700">
          <BulbIcon className="h-3.5 w-3.5" />
          Tip
        </p>
        <p className="mt-1 text-sm leading-6 text-slate-600">{tip}</p>
      </div>
    </div>
  );
}

function AvatarOrb({ isSpeaking }: { isSpeaking: boolean }) {
  return (
    <div className="relative flex h-28 w-28 items-center justify-center rounded-full bg-gradient-to-br from-indigo-400 via-violet-500 to-purple-600 shadow-lg shadow-indigo-500/30">
      {isSpeaking && (
        <>
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-indigo-400 opacity-30" />
          <span className="absolute -inset-2 animate-pulse rounded-full border-2 border-indigo-300/60" />
        </>
      )}
      <svg viewBox="0 0 24 24" fill="none" className="relative h-12 w-12 text-white">
        <circle cx="12" cy="8.5" r="3.5" fill="currentColor" />
        <path
          d="M5 20c0-3.9 3.1-7 7-7s7 3.1 7 7"
          stroke="currentColor"
          strokeWidth={2}
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
}

function Waveform({ active }: { active: boolean }) {
  const heights = [8, 16, 24, 16, 8];
  return (
    <div className="flex h-6 items-center gap-1">
      {heights.map((height, index) => (
        <span
          key={index}
          className="w-1 rounded-full bg-indigo-400"
          style={{
            height,
            opacity: active ? 1 : 0.25,
            animation: active ? "waveform-bar 0.9s ease-in-out infinite" : "none",
            animationDelay: `${index * 0.1}s`,
          }}
        />
      ))}
    </div>
  );
}

function Badge({ icon, label }: { icon: React.ReactNode; label: string }) {
  return (
    <div className="flex items-center justify-center gap-1.5 rounded-full bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-600">
      {icon}
      {label}
    </div>
  );
}