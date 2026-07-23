from pydantic import BaseModel, Field

from app.engine.client import MODEL, get_openai_client


class OpeningQuestion(BaseModel):
    remark: str = Field(
        description=(
            "Short, natural spoken greeting to open the interview — one "
            "sentence, warm but brief. Never stored in the transcript — "
            "display/speech only."
        )
    )
    question: str


def generate_opening_question(role_title: str) -> OpeningQuestion:
    client = get_openai_client()
    response = client.responses.parse(
        model=MODEL,
        instructions=(
            "You are an experienced technical interviewer conducting a job "
            f"interview for a {role_title} position. Write a brief, warm "
            "one-sentence greeting to open the interview, then ask one "
            "clear, specific opening question. Keep the question concise — "
            "one or two sentences."
        ),
        input="Begin the interview.",
        text_format=OpeningQuestion,
    )
    return response.output_parsed