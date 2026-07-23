from pydantic import BaseModel

from app.engine.client import MODEL, get_openai_client


class OpeningQuestion(BaseModel):
    question: str


def generate_opening_question(role_title: str) -> str:
    client = get_openai_client()
    response = client.responses.parse(
        model=MODEL,
        instructions=(
            "You are an experienced technical interviewer conducting a job "
            f"interview for a {role_title} position. Ask one clear, specific "
            "opening question to start the interview. Keep it concise — one "
            "or two sentences. Do not greet the candidate or explain "
            "yourself, just ask the question."
        ),
        input="Begin the interview.",
        text_format=OpeningQuestion,
    )
    return response.output_parsed.question