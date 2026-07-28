"use client";

export type AnswerStage = "idle" | "transcribing" | "reviewing" | "submitting";

// Record/transcript controls for the current answer. Split out of what
// used to be CameraPanel so the camera self-view can live on its own,
// full-height, in the rightmost column while this sits under the
// interviewer avatar in the middle column.
export function AnswerPanel({
  isRecording,
  stage,
  transcript,
  onTranscriptChange,
  onStartRecording,
  onStopRecording,
  onRerecord,
  onSubmitAnswer,
  recorderError,
  error,
}: {
  isRecording: boolean;
  stage: AnswerStage;
  transcript: string;
  onTranscriptChange: (value: string) => void;
  onStartRecording: () => void;
  onStopRecording: () => void;
  onRerecord: () => void;
  onSubmitAnswer: () => void;
  recorderError: string | null;
  error: string | null;
}) {
  return (
    <div className="flex flex-col gap-4">
      {isRecording ? (
        <button
          onClick={onStopRecording}
          className="flex w-full items-center justify-between rounded-2xl bg-gradient-to-r from-red-600 to-rose-600 px-6 py-4 text-left text-white shadow-lg shadow-red-600/25 transition-opacity hover:opacity-95"
        >
          <span>
            <span className="block text-sm font-semibold">Stop Recording</span>
            <span className="block text-xs text-white/80">Click when you&apos;re done answering</span>
          </span>
          <span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/20">
            <span className="h-3 w-3 rounded-sm bg-white" />
          </span>
        </button>
      ) : stage === "idle" ? (
        <button
          onClick={onStartRecording}
          className="flex w-full items-center justify-between rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 px-6 py-4 text-left text-white shadow-lg shadow-indigo-600/25 transition-opacity hover:opacity-95"
        >
          <span>
            <span className="block text-sm font-semibold">Record Answer</span>
            <span className="block text-xs text-white/80">Click to start recording your response</span>
          </span>
          <span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/20">
            <span className="h-4 w-4 rounded-full bg-white" />
          </span>
        </button>
      ) : stage === "transcribing" ? (
        <div className="flex items-center justify-center gap-3 rounded-2xl border border-slate-200 bg-white/80 py-4 text-sm text-slate-600">
          <span className="h-4 w-4 animate-spin rounded-full border-2 border-indigo-200 border-t-indigo-600" />
          Transcribing your answer…
        </div>
      ) : (
        <div className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white/80 p-5">
          <label htmlFor="transcript" className="text-sm font-medium text-slate-700">
            Your answer
          </label>
          <textarea
            id="transcript"
            value={transcript}
            onChange={(e) => onTranscriptChange(e.target.value)}
            disabled={stage === "submitting"}
            rows={4}
            className="rounded-xl border border-slate-300 px-3.5 py-2.5 text-sm text-slate-900 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
          />
          <div className="flex gap-3">
            <button
              onClick={onRerecord}
              disabled={stage === "submitting"}
              className="flex-1 rounded-full border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-700 transition-colors hover:bg-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              Re-record
            </button>
            <button
              onClick={onSubmitAnswer}
              disabled={stage === "submitting" || transcript.trim().length === 0}
              className="flex-1 rounded-full bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition-colors hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {stage === "submitting" ? "Submitting…" : "Submit Answer"}
            </button>
          </div>
        </div>
      )}

      {recorderError && <p className="text-sm text-red-600">{recorderError}</p>}
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
}
