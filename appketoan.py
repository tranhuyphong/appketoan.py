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
def render_duolingo_pro(unit_id, lessons):
    html = """
    <style>
    .map { display: flex; flex-direction: column; align-items: center; gap: 35px; }
    .row { width: 100%; display: flex; }
    .left { justify-content: flex-start; padding-left: 20%; }
    .right { justify-content: flex-end; padding-right: 20%; }

    .node {
        width: 75px; height: 75px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; color: white; cursor: pointer;
    }

    .done { background: #22c55e; }
    .current { background: #3b82f6; }
    .locked { background: #334155; opacity: 0.4; cursor: not-allowed; }
    .boss { background: gold; color: black; }
    .exam { background: purple; }

    .line { width: 6px; height: 40px; background: #475569; }
    </style>

    <div class="map">
    """

    for i, lesson in enumerate(lessons):
        cls = f"node {lesson['status']}"

        if lesson.get("type") == "boss":
            cls += " boss"
        elif lesson.get("type") == "exam":
            cls += " exam"

        side = "left" if i % 2 == 0 else "right"
        label = lesson.get("label", i+1)

        click = f"sendClick('{unit_id}|{i}')" if lesson["status"] != "locked" else ""

        html += f"""
        <div class="row {side}">
            <div class="{cls}" onclick="{click}">
                {label}
            </div>
        </div>
        """

        if i < len(lessons)-1:
            html += "<div class='line'></div>"

    html += "</div>"

    return components.html(f"""
{html}
<script>
function sendClick(val){{
    window.parent.postMessage({{
        type: "streamlit:setComponentValue",
key: "clicked_node",
value: val
    }}, "*");
}}
</script>
""", height=600)

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
if menu == "📘 Học":
    st.header("🗺️ Learning Map")

    if st.session_state.current_lesson:
        lesson = st.session_state.current_lesson
        st.subheader(lesson["title"])
        st.write(lesson["content"])
        if st.button("❌ Đóng"):
            st.session_state.current_lesson = None
            st.rerun()

    for level in curriculum:
        level_name = level.get("level", "Level")
        required = level.get("unlock_coins", 0)
        unlocked = coins >= required

        st.markdown(f"## {'🔓' if unlocked else '🔒'} {level_name}")

        for module in level.get("modules", []):
            st.markdown(f"### 📚 {module['name']}")

            lesson_nodes = []
            prev_passed = True

            lessons_full = module["lessons"].copy()

            # add boss + exam
            lessons_full.append({"title": "Boss", "type": "boss"})
            lessons_full.append({"title": "Exam", "type": "exam"})

            for i, lesson in enumerate(lessons_full):
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"
                prog = st.session_state.lesson_progress.get(l_id, {"submitted": False, "score": 0})

                if prog["submitted"]:
                    status = "done"
                elif prev_passed and unlocked:
                    status = "current"
                else:
                    status = "locked"

                lesson_nodes.append({
                    "status": status,
                    "type": lesson.get("type", "normal"),
                    "label": "👑" if lesson.get("type") == "boss" else "🎓" if lesson.get("type") == "exam" else i+1
                })

                prev_passed = (status == "done")

            render_duolingo_pro(module["name"], lesson_nodes)
            clicked = st.session_state.get("clicked_node")

            if clicked and "|" in clicked:
    unit, index = clicked.split("|")

    if unit != module["name"]:
        continue

    idx = int(index)

    if idx < len(module["lessons"]):
        st.session_state.current_lesson = module["lessons"][idx]

    st.session_state.clicked_node = None
    st.rerun()

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
