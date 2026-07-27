"use client";

import { useState } from "react";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { InterviewResults } from "@/features/interview/components/InterviewResults";
import { InterviewSession } from "@/features/interview/components/InterviewSession";
import { InterviewSetupForm } from "@/features/interview/components/InterviewSetupForm";
import type { Feedback, InterviewStartResponse } from "@/features/interview/api";

type FlowState =
  | { stage: "setup" }
  | { stage: "session"; start: InterviewStartResponse }
  | { stage: "complete"; feedback: Feedback };

function InterviewFlow() {
  const [state, setState] = useState<FlowState>({ stage: "setup" });

  if (state.stage === "setup") {
    return (
      <InterviewSetupForm
        onStarted={(start) => setState({ stage: "session", start })}
      />
    );
  }

  if (state.stage === "session") {
    return (
      <InterviewSession
        interview={state.start.interview}
        initialRemark={state.start.remark}
        initialQuestion={state.start.question}
        onCompleted={(feedback) => setState({ stage: "complete", feedback })}
      />
    );
  }

  return <InterviewResults feedback={state.feedback} />;
}

export default function NewInterviewPage() {
  return (
    <ProtectedRoute>
      <InterviewFlow />
    </ProtectedRoute>
  );
}