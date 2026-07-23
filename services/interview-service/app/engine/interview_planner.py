from pydantic import BaseModel, Field

from app.core.constants import MAX_QUESTIONS, MIN_QUESTIONS
from app.engine.client import MODEL, get_openai_client


class InterviewPlan(BaseModel):
    question_count: int = Field(
        ge=MIN_QUESTIONS,
        le=MAX_QUESTIONS,
        description=(
            f"Total planned questions for this interview, {MIN_QUESTIONS}-{MAX_QUESTIONS}. "
            f"Default to {MIN_QUESTIONS} unless the resume/role combination clearly warrants "
            "more depth (senior role, extensive directly-relevant experience) — then scale up."
        ),
    )
    remark: str = Field(description="Short, warm one-sentence greeting to open the interview.")
    question: str = Field(
        description=(
            "The first interview question. Reference something specific and relevant from "
            "the resume where possible, tailored to the role — not a generic opener."
        )
    )
    reasoning: str = Field(description="Brief internal reasoning, never shown to the candidate")


def plan_interview(*, role_title: str, resume_text: str) -> InterviewPlan:
    """The combined 'processing' step: reads the resume + role once, decides
    how many questions this interview should have, and generates a
    resume-aware opening question — one LLM call instead of two, since the
    result needs to come back as a single ~5-6 second wait, not two stacked
    round trips."""
    client = get_openai_client()
    response = client.responses.parse(
        model=MODEL,
        instructions=(
            "You are an experienced technical interviewer preparing to interview a candidate "
            f"for a {role_title} position. You've been given their resume. Decide how many "
            "questions this interview should have, and write a warm opening greeting plus the "
            "first question — grounded in something specific from their resume."
        ),
        input=f"Resume:\n{resume_text}",
        text_format=InterviewPlan,
    )
    plan = response.output_parsed
    # Defensive clamp, matching the pattern used for question_count
    # enforcement elsewhere — confirmed live that the API respects
    # ge/le here, but don't rely solely on that holding forever.
    plan.question_count = max(MIN_QUESTIONS, min(plan.question_count, MAX_QUESTIONS))
    return plan