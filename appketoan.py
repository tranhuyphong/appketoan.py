import streamlit as st
import random
import datetime
import pandas as pd
import streamlit.components.v1 as components
from supabase import create_client

# ================= 1. CẤU HÌNH =================
st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ================= 2. IMPORT =================
try:
    from data.career_tasks import career_tasks
    from data.curriculum import curriculum
    from data.question_bank import question_bank
    from data.dictionary import dictionary
    from data.case_study import case_studies
    from engine.ai_teacher import teacher_explain
    from engine.progress_tracker import update_progress
    from engine.classroom_ai import classroom_chat
    from engine.boss_ai import boss_msg
    from engine.ai_grader import grade
    from engine.financial_report import generate_report
    from engine.fraud_detection import detect_fraud
    from data.finance_data import transactions
except ImportError as e:
    st.error(f"⚠️ Thiếu file hệ thống: {e}")
    curriculum = []
    question_bank = []

# 👉 Ưu tiên learning_path
try:
    from data.learning_path import learning_path
    if learning_path:
        curriculum = learning_path
except Exception as e:
    st.error(f"Lỗi learning_path: {e}")

# ================= 3. SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indqd3Rvd21kY2RrcHJ5eGNxcXR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3NjY1NDMsImV4cCI6MjA5MjM0MjU0M30.jX4wAiXNezvmnwvr1hucjRxANZ5jWgzwn_9BsVCoueg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= 4. MAP FIX =================
def render_map_streamlit(module_name, lessons):
    st.markdown("###")

    cols = st.columns(5)

    for i, lesson in enumerate(lessons):
        col = cols[i % 5]

        status = lesson["status"]
        label = lesson["label"]
        ltype = lesson.get("type", "normal")

        # 🎨 màu + icon
        if status == "done":
            icon = "🟢"
        elif status == "current":
            icon = "🔵"
        else:
            icon = "⚫"

        if ltype == "boss":
            icon = "👑"
        elif ltype == "exam":
            icon = "🎓"

        disabled = (status == "locked")

        with col:
            if st.button(
                f"{icon}",
                key=f"{module_name}_{i}",
                disabled=disabled,
                use_container_width=True
            ):
                return f"{module_name}|{i}"

    return None

# ================= DB =================
def load_progress():
    try:
        res = supabase.table("users_progress").select("*").eq("email", st.session_state.user).execute()
        return {r["lesson_id"]: r for r in res.data}
    except:
        return {}

def save_progress(lesson_id, score):
    try:
        supabase.table("users_progress").upsert({
            "email": st.session_state.user,
            "lesson_id": lesson_id,
            "status": "done",
            "score": score,
            "last_learned": str(datetime.date.today())
        }).execute()
    except:
        pass

def save_coins():
    try:
        supabase.table("users").upsert({
            "email": st.session_state.user,
            "coins": st.session_state.coins
        }).execute()
    except:
        pass

# ================= SESSION =================
if "coins" not in st.session_state:
    st.session_state.update({
        "coins": 100,
        "streak": 0,
        "last_login": "",
        "lesson_progress": {},
        "current_lesson": None,
        "clicked_node": None,
        "q_index": 0,
        "chat_history": []
    })

# ================= LOGIN =================
if "user" not in st.session_state:
    st.title("🚀 PHONG AI ACCOUNTING")
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])

    with tab1:
        email = st.text_input("Email")
        pw = st.text_input("Password", type="password")
        if st.button("Đăng nhập"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": pw})
                if res.user:
                    st.session_state.user = res.user.email
                    st.rerun()
            except:
                st.error("Sai tài khoản hoặc mật khẩu!")

    with tab2:
        reg_email = st.text_input("Email đăng ký")
        reg_pw = st.text_input("Password đăng ký", type="password")
        if st.button("Đăng ký"):
            try:
                supabase.auth.sign_up({"email": reg_email, "password": reg_pw})
                st.success("Đăng ký xong!")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    st.stop()

# ================= LOAD PROGRESS =================
if "progress_loaded" not in st.session_state:
    db_progress = load_progress()
    for l_id, data in db_progress.items():
        st.session_state.lesson_progress[l_id] = {
            "submitted": True,
            "score": data.get("score", 0)
        }
    st.session_state.progress_loaded = True

# ================= UI =================
coins = st.session_state.coins
st.sidebar.markdown(f"💰 Coins: {coins}")

menu = st.sidebar.radio("Menu", [
    "📘 Học",
    "🎓 Lớp học AI (Quiz)",
    "🎓 Lớp học AI (Chat)",
    "💼 Đi làm",
    "🧾 Case Study",
    "📊 Dashboard",
    "📊 Financial Report",
    "🤖 Chấm bút toán",
    "📚 Từ điển",
    "🚨 Fraud Detection",
    "🏆 Leaderboard"
])

# ================= 📘 LEARNING =================
import time

if menu == "📘 Học":
    st.header("🗺️ Learning Map")

    # ================= LESSON VIEW =================
    if st.session_state.get("current_lesson"):
        lesson = st.session_state.current_lesson
        l_id = st.session_state.current_lesson_id

        # init state
        if st.session_state.get("lesson_start") is None:
            st.session_state.lesson_start = time.time()

        if "start_quiz" not in st.session_state:
            st.session_state.start_quiz = False

        if "quiz_index" not in st.session_state:
            st.session_state.quiz_index = 0
            st.session_state.correct = 0

        elapsed = time.time() - st.session_state.lesson_start

        st.success(f"📖 {lesson['title']}")

        # ===== CONTENT =====
        if elapsed < 15 and not st.session_state.start_quiz:
            st.write(lesson["content"])
            st.info(f"⏳ Đọc bài: {int(15 - elapsed)}s")

            if st.button("👉 Làm quiz ngay"):
                st.session_state.start_quiz = True
                st.rerun()

        # ===== QUIZ =====
        else:
            st.warning("🧠 Quiz")

            questions = lesson.get("quiz", [])
            if not questions:
                st.info("Bài này chưa có quiz")
                st.stop()

            i = st.session_state.quiz_index

            if i < len(questions):
                q = questions[i]

                st.write(f"### ❓ {q['question']}")
                choice = st.radio(
                    "Chọn đáp án",
                    q["options"],
                    key=f"{l_id}_quiz_{i}"
                )

                if st.button("👉 Trả lời"):
                    if q["options"].index(choice) == q["answer"]:
                        st.session_state.correct += 1

                    st.session_state.quiz_index += 1
                    st.rerun()

            else:
                score = int(st.session_state.correct / len(questions) * 100)

                st.subheader(f"📊 {score}%")

                if score >= 70:
                    st.success("🎉 PASS +20 coins")
                    st.session_state.coins += 20

                    st.session_state.lesson_progress[l_id] = {
                        "submitted": True,
                        "score": score
                    }

                    save_progress(l_id, score)
                    save_coins()

                else:
                    st.error("❌ FAIL (≥70%)")

                if st.button("🔙 Quay lại map"):
                    st.session_state.current_lesson = None
                    st.session_state.lesson_start = None
                    st.session_state.quiz_index = 0
                    st.session_state.correct = 0
                    st.session_state.start_quiz = False
                    st.rerun()

    # ================= MAP =================
    for level in curriculum:
        level_name = level.get("level", "Level")
        unlocked = coins >= level.get("unlock_coins", 0)

        st.markdown(f"## {'🔓' if unlocked else '🔒'} {level_name}")

        for module in level["modules"]:
            st.markdown(f"### 📚 {module['name']}")

            lessons = module["lessons"]
            cols = st.columns(5)

            all_passed = True

            # ===== LESSON =====
            for i, lesson in enumerate(lessons):
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"

                prog = st.session_state.lesson_progress.get(
                    l_id, {"submitted": False, "score": 0}
                )

                if prog["submitted"] and prog["score"] >= 70:
                    status = "done"
                elif unlocked:
                    status = "current"
                    all_passed = False
                else:
                    status = "locked"
                    all_passed = False

                icon = "🟢" if status == "done" else "🔵" if status == "current" else "⚫"

                with cols[i % 5]:
                    if st.button(icon, key=l_id, disabled=(status == "locked")):
                        st.session_state.current_lesson = lesson
                        st.session_state.current_lesson_id = l_id
                        st.session_state.lesson_start = None
                        st.session_state.quiz_index = 0
                        st.session_state.correct = 0
                        st.session_state.start_quiz = False
                        st.rerun()

            # ===== BOSS =====
            boss_id = f"{level_name}_{module['name']}_boss"
            with cols[len(lessons) % 5]:
                if st.button("👑", key=boss_id, disabled=not all_passed):
                    score = random.randint(60, 100)

                    if score >= 70:
                        st.success(f"👑 Boss PASS {score}% (+50)")
                        st.session_state.coins += 50
                        st.session_state.lesson_progress[boss_id] = {"submitted": True, "score": score}
                        save_coins()
                    else:
                        st.error("💀 Boss FAIL")

            # ===== EXAM =====
            exam_id = f"{level_name}_{module['name']}_exam"
            with cols[(len(lessons)+1) % 5]:
                if st.button("🎓", key=exam_id, disabled=not all_passed):
                    score = random.randint(60, 100)

                    if score >= 70:
                        st.success(f"🎓 Exam PASS {score}% (+100)")
                        st.session_state.coins += 100
                        st.session_state.lesson_progress[exam_id] = {"submitted": True, "score": score}
                        save_coins()
                    else:
                        st.error("❌ Exam FAIL")
# ================= CÁC MENU KHÁC GIỮ NGUYÊN =================
elif menu == "🎓 Lớp học AI (Quiz)":
    st.write("Quiz")

elif menu == "🎓 Lớp học AI (Chat)":
    st.write("Chat")

elif menu == "💼 Đi làm":
    st.write("Career")

elif menu == "🧾 Case Study":
    st.write("Case Study")

elif menu == "📊 Dashboard":
    st.write("Dashboard")

elif menu == "📊 Financial Report":
    st.write("Report")

elif menu == "🤖 Chấm bút toán":
    st.write("Grader")

elif menu == "📚 Từ điển":
    st.write("Dictionary")

elif menu == "🚨 Fraud Detection":
    st.write("Fraud")

elif menu == "🏆 Leaderboard":
    st.write("Leaderboard")

# ================= LOGOUT =================
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()
