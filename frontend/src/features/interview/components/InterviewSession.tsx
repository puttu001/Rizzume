"use client";

import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import { pollTranscription, uploadForTranscription } from "@/features/audio/api";
import { AnswerPanel } from "@/features/interview/components/AnswerPanel";
import { AvatarPanel } from "@/features/interview/components/AvatarPanel";
import { CameraPanel } from "@/features/interview/components/CameraPanel";
import { InterviewTopBar } from "@/features/interview/components/InterviewTopBar";
import { LockIcon } from "@/features/interview/components/icons";
import { QuestionPanel } from "@/features/interview/components/QuestionPanel";
import { useAudioRecorder } from "@/features/interview/hooks/useAudioRecorder";
import { useElapsedTimer, formatElapsed } from "@/features/interview/hooks/useElapsedTimer";
import { useSpeech } from "@/features/interview/hooks/useSpeech";
import { submitAnswer, type Feedback, type InterviewOut } from "@/features/interview/api";
import { ApiError } from "@/lib/api-client";

type Stage = "idle" | "transcribing" | "reviewing" | "submitting";

export function InterviewSession({
  interview,
  initialRemark,
  initialQuestion,
  onCompleted,
}: {
  interview: InterviewOut;
  initialRemark: string;
  initialQuestion: string;
  onCompleted: (feedback: Feedback) => void;
}) {
  const [questions, setQuestions] = useState<string[]>([initialQuestion]);
  const [stage, setStage] = useState<Stage>("idle");
  const [transcript, setTranscript] = useState("");
  const [error, setError] = useState<string | null>(null);

  const recorder = useAudioRecorder();
  const speech = useSpeech();
  const router = useRouter();
  const elapsedSeconds = useElapsedTimer();

  const hasSpokenOpeningRef = useRef(false);
  useEffect(() => {
    // React StrictMode double-invokes effects in dev, which fired this
    // twice and played two overlapping TTS calls — this ref (persists
    // across the double-invoke since the component instance isn't
    // remounted) makes sure the opening remark+question is only ever
    // spoken, and only ever fetched from audio-service, once. Every
    // question after this is spoken explicitly from handleSubmitAnswer.
    if (hasSpokenOpeningRef.current) return;
    hasSpokenOpeningRef.current = true;
    void speech.speak(`${initialRemark} ${initialQuestion}`.trim());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleStopRecording() {
    setStage("transcribing");
    setError(null);
    try {
      const blob = await recorder.stop();
      const { job_id } = await uploadForTranscription(blob);
      const text = await pollTranscription(job_id);
      setTranscript(text);
      setStage("reviewing");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Try again.");
      recorder.reset();
      setStage("idle");
    }
  }

  function handleRerecord() {
    setTranscript("");
    setError(null);
    recorder.reset();
    setStage("idle");
  }

  async function handleSubmitAnswer() {
    setStage("submitting");
    setError(null);
    try {
      const response = await submitAnswer(interview.id, transcript);
      if (response.feedback) {
        onCompleted(response.feedback);
        return;
      }
      const remark = response.remark ?? "";
      const question = response.question ?? "";
      setQuestions((prev) => [...prev, question]);
      setTranscript("");
      recorder.reset();
      setStage("idle");
      void speech.speak(`${remark} ${question}`.trim());
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong. Try again.");
      setStage("reviewing");
    }
  }

  function handleEndInterview() {
    const confirmed = window.confirm(
      "End this interview now? Ending early won't generate feedback — only interviews " +
        "that run to completion do.",
    );
    if (!confirmed) return;

    if (recorder.status === "recording") {
      void recorder.stop();
    }
    speech.stop();
    router.push("/dashboard");
  }

  return (
    <div className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-6 px-6 py-6">
      <InterviewTopBar
        elapsedLabel={formatElapsed(elapsedSeconds)}
        questionNumber={questions.length}
        maxQuestions={interview.max_questions}
        onEndInterview={handleEndInterview}
      />

      <div className="grid flex-1 gap-6 lg:grid-cols-[300px_360px_1fr]">
        <QuestionPanel questions={questions} />

        <div className="flex flex-col gap-6">
          <AvatarPanel
            isSpeaking={speech.isSpeaking}
            isRecording={recorder.status === "recording"}
            questionIndex={questions.length - 1}
          />

          <AnswerPanel
            isRecording={recorder.status === "recording"}
            stage={stage}
            transcript={transcript}
            onTranscriptChange={setTranscript}
            onStartRecording={() => recorder.start()}
            onStopRecording={handleStopRecording}
            onRerecord={handleRerecord}
            onSubmitAnswer={handleSubmitAnswer}
            recorderError={recorder.error}
            error={error}
          />
        </div>

        <CameraPanel />
      </div>

      <p className="flex items-center justify-center gap-1.5 text-center text-xs text-slate-400">
        <LockIcon className="h-3.5 w-3.5" />
        Your data is encrypted and secure. We respect your privacy.
      </p>
    </div>
  );
}