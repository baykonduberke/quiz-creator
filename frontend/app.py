import streamlit as st
import requests

API_URL = "http://localhost:8000/api/quiz"

st.set_page_config(page_title="Quiz Creator", page_icon="🧠", layout="centered")
st.title("Quiz Creator")
st.markdown("Markdown metin yukleyin, quiz olusturalim!")

if "quiz" not in st.session_state:
    st.session_state.quiz = None
    st.session_state.current_q = 0
    st.session_state.answers = {}
    st.session_state.submitted = False

content = st.text_area("Markdown metni buraya yapistirin:", height=300)
num_questions = st.slider("Soru sayisi:", min_value=1, max_value=20, value=5)

if st.button("Quiz Olustur") and content:
    with st.spinner("Sorular uretiliyor..."):
        response = requests.post(
            f"{API_URL}/generate",
            json={"content": content, "num_questions": num_questions},
        )
        if response.status_code == 200:
            data = response.json()
            if data["quiz"]["questions"]:
                st.session_state.quiz = data
                st.session_state.current_q = 0
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.session_state.checked = {}
            else:
                st.error("Sorular uretilemedi. Lutfen tekrar deneyin.")
        else:
            st.error("Quiz olusturulamadi!")

if "checked" not in st.session_state:
    st.session_state.checked = {}

if st.session_state.quiz and not st.session_state.submitted:
    quiz = st.session_state.quiz["quiz"]
    questions = quiz["questions"]
    idx = st.session_state.current_q

    st.divider()
    st.subheader(f"Soru {idx + 1}/{len(questions)}")

    q = questions[idx]
    st.markdown(f"**{q['question']}**")

    already_checked = idx in st.session_state.checked

    answer = st.radio(
        "Cevabin:",
        options=q["options"],
        key=f"q_{idx}",
        disabled=already_checked,
    )
    st.session_state.answers[idx] = answer

    if not already_checked:
        if st.button("Cevabi Kontrol Et"):
            st.session_state.checked[idx] = True
            st.rerun()

    if already_checked:
        user_answer = st.session_state.answers[idx]
        is_correct = user_answer == q["correct_answer"]

        if is_correct:
            st.success("Dogru!")
        else:
            st.error(f"Yanlis! Dogru cevap: **{q['correct_answer']}**")

        st.info(f"**Aciklama:** {q['explanation']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if idx > 0 and st.button("Onceki"):
            st.session_state.current_q -= 1
            st.rerun()
    with col2:
        if idx < len(questions) - 1 and already_checked and st.button("Sonraki"):
            st.session_state.current_q += 1
            st.rerun()
    with col3:
        if idx == len(questions) - 1 and already_checked and st.button("Bitir"):
            st.session_state.submitted = True
            st.rerun()

if st.session_state.submitted:
    quiz = st.session_state.quiz["quiz"]
    questions = quiz["questions"]
    correct = 0

    st.divider()
    st.subheader("Sonuclar")

    for i, q in enumerate(questions):
        user_answer = st.session_state.answers.get(i, "")
        is_correct = user_answer == q["correct_answer"]
        if is_correct:
            correct += 1

        icon = "✅" if is_correct else "❌"
        with st.expander(f"{icon} Soru {i + 1}: {q['question']}"):
            st.write(f"**Senin cevabin:** {user_answer}")
            st.write(f"**Dogru cevap:** {q['correct_answer']}")
            st.write(f"**Aciklama:** {q['explanation']}")

    score = int((correct / len(questions)) * 100)
    st.metric("Skorun", f"{score}%", f"{correct}/{len(questions)} dogru")

    if st.button("Yeni Quiz"):
        st.session_state.quiz = None
        st.session_state.submitted = False
        st.session_state.checked = {}
        st.rerun()
