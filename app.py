# app.py
import streamlit as st
from utils import load_questions, get_random_questions, save_result

st.set_page_config(page_title="Quiz App", layout="centered")
st.title("Quiz App — Streamlit")
st.write("50 questions stored, 5 random questions per quiz.")

# User info
st.sidebar.header("Your info")
name = st.sidebar.text_input("Name")
email = st.sidebar.text_input("Email (optional)")

# Load all questions
all_questions = load_questions()
quiz_questions = get_random_questions(all_questions, num_questions=5)

# State
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

def submit_quiz():
    st.session_state.submitted = True

# Quiz form
with st.form("quiz_form"):
    for i, q in enumerate(quiz_questions, start=1):
        qid = q["id"]
        st.markdown(f"**Q{i}. {q['question']}**")
        selected = st.radio(
            label=f"Choose for Q{qid}",
            options=list(range(len(q["options"]))),
            format_func=lambda idx, opts=q["options"]: opts[idx],
            key=f"q_{qid}"
        )
    st.form_submit_button("Submit", on_click=submit_quiz)

# After submit
if st.session_state.submitted:
    score = 0
    details = []
    for q in quiz_questions:
        qid = q["id"]
        user_sel = st.session_state.get(f"q_{qid}")
        correct = q["answer_index"]
        if user_sel == correct:
            score += 1
        details.append({
            "id": qid,
            "question": q["question"],
            "selected_index": user_sel,
            "selected_option": q["options"][user_sel],
            "correct_index": correct,
            "correct_option": q["options"][correct]
        })
    st.success(f"You scored {score} / {len(quiz_questions)}")
    st.write("---")
    for d in details:
        icon = "✅" if d["selected_index"] == d["correct_index"] else "❌"
        st.write(f"{icon} **{d['question']}**")
        st.write(f"Your answer: {d['selected_option']}")
        if d["selected_index"] != d["correct_index"]:
            st.write(f"Correct answer: {d['correct_option']}")
        st.write("---")

    if st.button("Save result"):
        save_result(name, email, score, len(quiz_questions), details)
        st.info("Result saved!")
