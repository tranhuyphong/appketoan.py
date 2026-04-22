import streamlit as st
import random
import datetime
import pandas as pd
import streamlit.components.v1 as components
from supabase import create_client

# ================= 1. CẤU HÌNH TRANG =================
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

# 👉 FIX dùng learning_path nếu có
try:
    from data.learning_path import learning_path
    curriculum = learning_path
except:
    pass

# ================= 3. SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indqd3Rvd21kY2RrcHJ5eGNxcXR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3NjY1NDMsImV4cCI6MjA5MjM0MjU0M30.jX4wAiXNezvmnwvr1hucjRxANZ5jWgzwn_9BsVCoueg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= 4. MAP (FIX) =================
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
        "percent": None,
        "lesson_progress": {},
        "current_lesson": None,
        "current_lesson_id": None,
        "q_index": 0,
        "chat_history": [],
        "skills": {},
        "learned_lessons": [],
        "daily_learn": 0
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
        if st.button("Thực hiện Đăng ký"):
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

# ================= DAILY BONUS =================
today = str(datetime.date.today())
if st.session_state.last_login != today:
    st.session_state.coins += 20
    st.session_state.last_login = today
    save_coins()

# ================= UI =================
coins = st.session_state.coins
rank = "🥉 Intern" if coins < 100 else "🥈 Junior" if coins < 300 else "🥇 Senior" if coins < 600 else "👑 Manager"

st.sidebar.markdown(f"### 🎖️ Rank: {rank}")
st.sidebar.markdown(f"### 💰 Coins: {coins}")

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

# ================= 📘 LEARNING MAP (ĐÃ FIX) =================
if menu == "📘 Học":
    st.header("🗺️ Learning Map")

    if st.session_state.get("current_lesson"):
        lesson = st.session_state.current_lesson
        st.markdown(f"## 📖 {lesson['title']}")
        st.write(lesson["content"])

        if st.button("❌ Đóng"):
            st.session_state.current_lesson = None
            st.rerun()

    for level in curriculum:
        level_name = level.get("level") or level.get("name") or "Level"
        required = level.get("unlock_coins", 0)
        unlocked = coins >= required

        st.markdown(f"## {'🔓' if unlocked else '🔒'} {level_name} (Cần {required} 💰)")

        for module in level.get("modules", []):
            st.markdown(f"### 📚 {module['name']}")

            lesson_nodes = []
            prev_passed = True

            for i, lesson in enumerate(module["lessons"]):
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"
                prog = st.session_state.lesson_progress.get(l_id, {"submitted": False, "score": 0})

                if prog["submitted"] and prog["score"] >= 70:
                    status = "done"
                elif prev_passed and unlocked:
                    status = "current"
                else:
                    status = "locked"

                lesson_nodes.append({
                    "status": status,
                    "type": "lesson",
                    "label": str(i+1)
                })

                prev_passed = (status == "done")

            # Boss
            lesson_nodes.append({
                "status": "current" if prev_passed else "locked",
                "type": "boss",
                "label": "👑"
            })

            # Exam cuối level
            if module == level["modules"][-1]:
                lesson_nodes.append({
                    "status": "locked",
                    "type": "exam",
                    "label": "🎓"
                })

            clicked = render_duolingo_pro(module["name"], lesson_nodes)

            if clicked and isinstance(clicked, str) and "|" in clicked:
                unit, index = clicked.split("|")
                if unit == module["name"]:
                    idx = int(index)
                    if idx < len(module["lessons"]):
                        st.session_state.current_lesson = module["lessons"][idx]
                        st.rerun()

# ================= GIỮ NGUYÊN CÁC MENU KHÁC =================
elif menu == "🎓 Lớp học AI (Quiz)":
    if len(question_bank) > 0:
        q = question_bank[st.session_state.q_index % len(question_bank)]
        st.subheader(q["question"])
        ans = st.radio("Chọn đáp án:", q["options"])
        if st.button("Nộp"):
            if q["options"].index(ans) == q["correct"]:
                st.session_state.streak += 1
                reward = min(10 + st.session_state.streak * 2, 30)
                st.success(f"Chính xác! +{reward} coins")
                st.session_state.coins += reward
            else:
                st.session_state.streak = 0
                st.error("Sai rồi! -5 coins")
                st.session_state.coins -= 5
            st.info(q["explain"])
            save_coins()
        if st.button("➡️ Câu tiếp"):
            st.session_state.q_index += 1
            st.rerun()

elif menu == "🎓 Lớp học AI (Chat)":
    st.header("💬 Chat với Giảng viên AI")
    if not st.session_state.chat_history:
        st.session_state.chat_history = [{"role": "assistant", "content": "Chào bạn"}]
    for m in st.session_state.chat_history:
        st.chat_message(m["role"]).write(m["content"])
    u_input = st.chat_input("Nhập...")
    if u_input:
        st.session_state.chat_history.append({"role": "user", "content": u_input})
        reply = classroom_chat(st.session_state.chat_history, u_input)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

elif menu == "💼 Đi làm":
    st.header("🏢 Career Mode")

elif menu == "🧾 Case Study":
    st.header("📄 Case Study")

elif menu == "📊 Dashboard":
    st.header("📊 Dashboard")

elif menu == "📊 Financial Report":
    st.header("📊 Report")

elif menu == "🤖 Chấm bút toán":
    st.header("🤖 Grader")

elif menu == "📚 Từ điển":
    st.header("📚 Dictionary")

elif menu == "🚨 Fraud Detection":
    st.header("🚨 Fraud Detection")

elif menu == "🏆 Leaderboard":
    st.header("🏆 Leaderboard")
    try:
        res = supabase.table("users").select("email, coins").execute()
        st.table(pd.DataFrame(res.data))
    except:
        st.error("Không tải được")

# ================= LOGOUT =================
st.sidebar.divider()
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()
