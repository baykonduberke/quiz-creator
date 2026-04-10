from pydantic import BaseModel, Field


class Question(BaseModel):
    question: str = Field(description="Soru metni")
    options: list[str] = Field(description="4 adet secenek")
    correct_answer: str = Field(description="Dogru cevap")
    explanation: str = Field(description="Cevap aciklamasi")


class Quiz(BaseModel):
    title: str = Field(description="Quiz basligi")
    questions: list[Question] = Field(description="Sorular listesi")


class QuizRequest(BaseModel):
    content: str = Field(description="Markdown metin icerigi")
    num_questions: int = Field(default=5, ge=1, le=20, description="Uretilecek soru sayisi")


class QuizResponse(BaseModel):
    quiz: Quiz
    total_questions: int
