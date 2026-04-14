from fastapi import APIRouter
from app.models.schemas import QuizRequest, QuizResponse, Quiz
from app.graph.builder import quiz_graph

router = APIRouter()


@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    try:
        result = quiz_graph.invoke({
            "raw_text": request.content,
            "num_questions": request.num_questions,
            "chunks": [],
            "questions": [],
            "quiz": {},
            "error": "",
        })
    except Exception as e:
        print(f"GRAPH HATASI: {e}")
        return QuizResponse(
            quiz=Quiz(title="Hata", questions=[]),
            total_questions=0,
        )

    if result.get("error"):
        print(f"HATA: {result['error']}")
        return QuizResponse(
            quiz=Quiz(title="Hata", questions=[]),
            total_questions=0,
        )

    quiz = Quiz(**result.get("quiz", {"title": "Quiz", "questions": []}))
    return QuizResponse(quiz=quiz, total_questions=len(quiz.questions))
