import { apiClient } from "@/lib/api-client";

// Mirrors audio-service's app/schemas/audio.py.
export interface TranscriptionJobCreated {
  job_id: string;
  status: "pending";
}

export interface TranscriptionStatus {
  job_id: string;
  status: "pending" | "started" | "completed" | "failed";
  transcript: string | null;
}

export function uploadForTranscription(
  audioBlob: Blob,
  filename = "answer.webm",
): Promise<TranscriptionJobCreated> {
  const formData = new FormData();
  formData.append("file", audioBlob, filename);
  return apiClient.postFormData<TranscriptionJobCreated>("/api/v1/audio/transcriptions", formData);
}

export function getTranscriptionStatus(jobId: string): Promise<TranscriptionStatus> {
  return apiClient.get<TranscriptionStatus>(`/api/v1/audio/transcriptions/${jobId}`);
}

// Synchronous on the backend (see audio-service's app/api/speech.py) —
// returns audio/mpeg bytes directly, no job polling needed.
export function synthesizeSpeech(text: string): Promise<Blob> {
  return apiClient.postForBlob("/api/v1/audio/speech", { text });
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export class TranscriptionFailedError extends Error {}
export class TranscriptionTimeoutError extends Error {}

// Polls until the Celery job settles. audio-service can't distinguish
// "not started yet" from "unknown job id" (see transcriptions.py's
// _STATE_MAP comment), so a generous timeout — not an attempt count — is
// what actually bounds this.
export async function pollTranscription(
  jobId: string,
  { intervalMs = 1500, timeoutMs = 60_000 }: { intervalMs?: number; timeoutMs?: number } = {},
): Promise<string> {
  const deadline = Date.now() + timeoutMs;

  while (Date.now() < deadline) {
    const result = await getTranscriptionStatus(jobId);
    if (result.status === "completed") {
      return result.transcript ?? "";
    }
    if (result.status === "failed") {
      throw new TranscriptionFailedError("Transcription failed. Try recording again.");
    }
    await sleep(intervalMs);
  }

  throw new TranscriptionTimeoutError("Transcription is taking too long. Try recording again.");
}