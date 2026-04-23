import streamlit as st
import random
import time
import datetime
from supabase import create_client

# ================= CONFIG =================
st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ================= SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indqd3Rvd21kY2RrcHJ5eGNxcXR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3NjY1NDMsImV4cCI6MjA5MjM0MjU0M30.jX4wAiXNezvmnwvr1hucjRxANZ5jWgzwn_9BsVCoueg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= DATA DEMO =================
curriculum = [
    {
        "level": "Level 1",
        "unlock_coins": 0,
        "modules": [
            {
                "name": "Basic Accounting",
                "lessons": [
                    {
                        "title": "Tài sản là gì?",
                        "content": "Tài sản là những gì doanh nghiệp sở hữu...",
                        "quiz": [
                            {"q": "Tài sản là gì?", "a": ["Nguồn lực", "Chi phí", "Nợ"], "correct": 0},
                            {"q": "Tài sản nằm bên nào?", "a": ["Nợ", "Có"], "correct": 0},
                            {"q": "Tiền mặt là?", "a": ["Tài sản", "Chi phí"], "correct": 0},
                            {"q": "Khoản phải thu là?", "a": ["Tài sản", "Nợ"], "correct": 0},
                            {"q": "Máy móc là?", "a": ["Tài sản", "Chi phí"], "correct": 0},
                        ]
                    },
                    {
                        "title": "Nợ phải trả",
                        "content": "Nợ là nghĩa vụ tài chính...",
                        "quiz": []
                    }
                ]
            }
        ]
    }
]

# ================= SESSION =================
if "init" not in st.session_state:
    st.session_state.update({
        "coins": 100,
        "lesson_progress": {},
        "current_lesson": None,
        "current_lesson_id": None,
        "lesson_start": None,
        "start_quiz": False,
        "quiz_index": 0,
        "correct": 0,
        "init": True
    })

# ================= UI =================
st.sidebar.markdown(f"💰 Coins: {st.session_state.coins}")

menu = st.sidebar.radio("Menu", ["📘 Học"])

# ================= LEARNING =================
if menu == "📘 Học":

    st.title("🗺️ Learning Map")

    # ================= LESSON VIEW =================
    import time

lesson = st.session_state.current_lesson

# ===== TIMER =====
if not st.session_state.get("lesson_start"):
    st.session_state.lesson_start = time.time()

elapsed = time.time() - st.session_state.lesson_start

st.markdown(f"## 📖 {lesson['title']}")

# ===== PROGRESS BAR =====
progress = min(elapsed / 60, 1.0)
st.progress(progress)
st.caption(f"⏳ {int(60 - elapsed)}s")

# ===== PHASE 1 =====
if elapsed < 60 and not st.session_state.get("start_quiz"):

    st.write(lesson["content"])

    if st.button("⚡ Skip → Quiz"):
        st.session_state.start_quiz = True
        st.rerun()

    time.sleep(1)
    st.rerun()

# ===== PHASE 2 QUIZ =====
else:

    st.markdown("### 🧠 Quiz Challenge")

    # ===== INIT =====
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.correct = 0

    questions = lesson.get("quiz", [])

    # ===== 🤖 AI GENERATE =====
    if not questions:
        base_q = [
            ("Tài sản là gì?", ["Nguồn lực", "Chi phí", "Nợ"], 0),
            ("Nợ là gì?", ["Nghĩa vụ", "Tài sản"], 0),
            ("Doanh thu là gì?", ["Thu nhập", "Chi phí"], 0),
        ]

        questions = []
        for q in base_q:
            questions.append({
                "q": q[0],
                "a": random.sample(q[1], len(q[1])),
                "correct": q[2]
            })

    i = st.session_state.quiz_index

    # ===== QUIZ LOOP =====
    if i < len(questions):

        q = questions[i]

        st.markdown(f"### ❓ {q['q']}")

        choice = st.radio("Chọn đáp án", q["a"], key=f"quiz_{i}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Trả lời"):

                if q["a"].index(choice) == q["correct"]:
                    st.session_state.correct += 1
                    st.success("🔥 Đúng!")
                else:
                    st.error("❌ Sai!")

                st.session_state.quiz_index += 1
                st.rerun()

        with col2:
            if st.button("⏭ Bỏ qua"):
                st.session_state.quiz_index += 1
                st.rerun()

    # ===== RESULT =====
    else:

        total = len(questions)
        correct = st.session_state.correct
        score = int(correct / total * 100)

        st.markdown("---")
        st.markdown(f"## 📊 Kết quả: {score}%")

        # ===== REWARD SYSTEM =====
        if score >= 70:

            reward = 20
            if score == 100:
                reward = 40  # bonus perfect

            st.success(f"🎉 PASS +{reward} coins")
            st.balloons()

            st.session_state.coins += reward

            l_id = st.session_state.current_lesson_id
            st.session_state.lesson_progress[l_id] = {
                "submitted": True,
                "score": score
            }

        else:
            st.error("❌ FAIL (cần ≥70%)")

        # ===== STREAK SYSTEM =====
        today = str(datetime.date.today())
        if st.session_state.get("last_learned") != today:
            st.session_state.streak += 1
            st.session_state.last_learned = today

        st.info(f"🔥 Streak: {st.session_state.streak} ngày")

        # ===== RESET =====
        if st.button("🔄 Học bài khác"):
            st.session_state.current_lesson = None
            st.session_state.lesson_start = None
            st.session_state.start_quiz = False
            st.session_state.quiz_index = 0
            st.session_state.correct = 0
            st.rerun()
    # ================= MAP =================
    else:
        for level in curriculum:

            st.markdown(f"## {level['level']}")

            for module in level["modules"]:
                st.markdown(f"### 📚 {module['name']}")

                cols = st.columns(5)

                for i, lesson in enumerate(module["lessons"]):
                    col = cols[i % 5]

                    l_id = f"{module['name']}_{lesson['title']}"

                    prog = st.session_state.lesson_progress.get(
                        l_id, {"submitted": False}
                    )

                    icon = "🟢" if prog["submitted"] else "🔵"

                    with col:
                        if st.button(icon, key=l_id):

                            st.session_state.current_lesson = lesson
                            st.session_state.current_lesson_id = l_id

                            # RESET STATE (QUAN TRỌNG)
                            st.session_state.lesson_start = None
                            st.session_state.start_quiz = False
                            st.session_state.quiz_index = 0
                            st.session_state.correct = 0

                            st.rerun()

# ================= LOGOUT =================
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()
