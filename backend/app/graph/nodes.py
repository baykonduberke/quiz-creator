import json
from langchain_openai import ChatOpenAI
from app.core.config import settings


llm = ChatOpenAI(
    model=settings.deepseek_model,
    base_url=settings.deepseek_base_url,
    api_key=settings.deepseek_api_key,
)


def chunk_text(state):
    raw_text = state["raw_text"]
    chunks = []
    current_chunk = ""

    for line in raw_text.split("\n"):
        if line.startswith("#") and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = ""
        current_chunk += line + "\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return {"chunks": chunks}


def generate_questions(state):
    chunks = state["chunks"]
    num_questions = state["num_questions"]
    all_questions = []

    questions_per_chunk = max(1, num_questions // len(chunks))

    for chunk in chunks:
        if len(all_questions) >= num_questions:
            break

        prompt = f"""Sen deneyimli bir yazilim muhendisi ve teknik egitmensin.
Asagidaki teknik metni okuyan bir yazilim gelistiricinin bu konuyu GERCEKTEN anlayip anlamadigini olcecek {questions_per_chunk} adet coktan secmeli soru uret.

SORU TASARIMI KURALLARI:
- Asla tarih, isim veya tanimlama ezberi sorma. "X nedir?" veya "X'i kim gelistirdi?" gibi sorular YASAK.
- Sorular su kaliplarda olmali:
  * "Su senaryoda ne olur?" (uygulama)
  * "Bu kod calistirildiginda cikti ne olur?" (analiz)
  * "A yerine B kullanmanin avantaji nedir?" (karsilastirma)
  * "Bu problemi cozmek icin en uygun yaklasim hangisidir?" (problem cozme)
  * "Bu kodda hata nerededir?" (debugging)
- Sorular gercek dunya yazilim gelistirme senaryolarindan turetilmeli
- Yanlis secenekler junior gelistiricilerin sik yaptigi hatalardan ve yanlis anlamalardan turetilmeli
- Her soru cevaplandiginda kisi yeni bir sey ogrenmeli

ACIKLAMA KURALLARI:
- Sadece dogru cevabi soyleme, NEDEN dogru oldugunu teknik olarak acikla
- Yanlis seceneklerin neden yanlis oldugunu da kisa acikla
- Pratik bir ipucu veya best practice ekle

Her soru icin su JSON formatinda don:
[
  {{
    "question": "Soru metni",
    "options": ["A secenegi", "B secenegi", "C secenegi", "D secenegi"],
    "correct_answer": "Dogru secenek",
    "explanation": "Detayli ogretici aciklama"
  }}
]

SADECE JSON dondur, baska hicbir sey yazma. Markdown kullanma.

Metin:
{chunk}
"""
        try:
            result = llm.invoke(prompt)
            content = result.content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1]
                content = content.rsplit("```", 1)[0]
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                parsed = [parsed]
            all_questions.extend(parsed)
        except Exception as e:
            print(f"Soru uretme hatasi: {e}")
            continue

    return {"questions": all_questions[:num_questions]}


def format_quiz(state):
    questions = state["questions"]
    quiz = {
        "title": "Quiz",
        "questions": questions,
    }
    return {"quiz": quiz}
