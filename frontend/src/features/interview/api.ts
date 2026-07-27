import { apiClient } from "@/lib/api-client";

// Mirrors interview-service's app/schemas/interview.py and
// app/engine/feedback_generator.py's InterviewFeedback — kept in sync by
// hand since each service is independent (no shared types package).
export interface Feedback {
  overall_score: number;
  strengths: string[];
  areas_for_improvement: string[];
  summary: string;
}

export interface InterviewOut {
  id: string;
  user_id: string;
  role_title: string;
  status: "in_progress" | "completed";
  current_difficulty: "easy" | "medium" | "hard";
  question_count: number;
  max_questions: number;
  feedback: Feedback | null;
  created_at: string;
  completed_at: string | null;
}

export interface InterviewStartResponse {
  interview: InterviewOut;
  remark: string;
  question: string;
}

export interface AnswerResponse {
  interview: InterviewOut;
  remark: string | null;
  question: string | null;
  feedback: Feedback | null;
}

// POST /api/v1/interviews/ — trailing slash required, interview-service's
// create route is its bare root and FastAPI 307-redirects without it.
export function startInterview(resume: File, roleTitle: string): Promise<InterviewStartResponse> {
  const formData = new FormData();
  formData.append("resume", resume);
  formData.append("role_title", roleTitle);
  return apiClient.postFormData<InterviewStartResponse>("/api/v1/interviews/", formData);
}

export function getInterview(interviewId: string): Promise<InterviewOut> {
  return apiClient.get<InterviewOut>(`/api/v1/interviews/${interviewId}`);
}

export function submitAnswer(interviewId: string, answer: string): Promise<AnswerResponse> {
  return apiClient.post<AnswerResponse>(`/api/v1/interviews/${interviewId}/answer`, { answer });
}