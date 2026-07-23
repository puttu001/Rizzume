from typing import Literal

from pydantic import BaseModel, Field

from app.engine.client import MODEL, get_openai_client
from app.engine.types import TranscriptTurn, format_transcript


class NextStepDecision(BaseModel):
    action: Literal["ask_question", "end_interview"]
    remark: str | None = Field(
        default=None,
        description=(
            "Short, natural spoken remark to precede the question — brief "
            "acknowledgment of the previous answer or a transition. One "
            "sentence, conversational, not a restatement of the question. "
            "Never stored in the transcript — display/speech only."
        ),
    )
    question: str | None = Field(
        default=None, description="Next question text — required when action is ask_question"
    )
    difficulty: Literal["easy", "medium", "hard"] | None = Field(
        default=None, description="Difficulty for the next question"
    )
    reasoning: str = Field(description="Brief internal reasoning, never shown to the candidate")


def decide_next_step(
    *,
    role_title: str,
    transcript: list[TranscriptTurn],
    current_difficulty: str,
    question_count: int,
    max_questions: int,
) -> NextStepDecision:
    """Follow-up question logic and difficulty control (two separate boxes
    in architecture.png) are deliberately one LLM call here, not two — a
    single call with structured output is faster, cheaper, and more
    coherent than asking the model to reason about difficulty separately
    from question content, which risks the two answers disagreeing with
    each other. See current_state.md for this deviation from the diagram."""
    client = get_openai_client()
    response = client.responses.parse(
        model=MODEL,
        instructions=(
            f"You are conducting a technical interview for a {role_title} position. "
            f"{question_count} question(s) asked so far, out of a maximum of {max_questions}. "
            f"Current difficulty: {current_difficulty}. "
            "Given the conversation so far, decide whether to ask a follow-up or a new "
            "question — raise difficulty if the candidate is doing well, lower it if they're "
            "struggling — or end the interview if the maximum question count has been reached "
            "or the conversation has reached a natural conclusion. Also write a short, "
            "natural spoken remark to go before the question — a brief, genuine "
            "acknowledgment of their previous answer or a transition into the next topic, "
            "the way a real interviewer would talk between questions. Keep it to one "
            "sentence and don't restate or preview the question itself."
        ),
        input=format_transcript(transcript),
        text_format=NextStepDecision,
    )
    return response.output_parsed