from typing import TypedDict


class QuizState(TypedDict):
    raw_text: str
    chunks: list[str]
    num_questions: int
    questions: list[dict]
    quiz: dict
    error: str
