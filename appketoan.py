import streamlit as st
import random
import datetime
import pandas as pd
import streamlit.components.v1 as components
from supabase import create_client

# ================= 1. CẤU HÌNH TRANG =================
st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ================= 2. IMPORT DỮ LIỆU & ENGINE =================
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
    curriculum = curriculum if 'curriculum' in locals() else []
    question_bank = question_bank if 'question_bank' in locals() else []

# ================= 3. KẾT NỐI SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indqd3Rvd21kY2RrcHJ5eGNxcXR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3NjY1NDMsImV4cCI6MjA5MjM0MjU0M30.jX4wAiXNezvmnwvr1hucjRxANZ5jWgzwn_9BsVCoueg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= 4. RENDER MAP (UPDATED) =================
def render_duolingo_pro(unit_id, lessons):
    html = f"""
    <style>
    .map {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 35px;
        padding: 20px;
    }}
    .row {{
        width: 100%;
        display: flex;
    }}
    .left {{ justify-content: flex-start; padding-left: 20%; }}
    .right {{ justify-content: flex-end; padding-right: 20%; }}

    .node {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 22px;
        color: white;
        cursor: pointer;
        transition: all 0.25s ease;
    }}

    .node:hover {{ transform: scale(1.15); }}

    .done {{ background: #22c55e; }}
    .current {{ background: #3b82f6; box-shadow: 0 0 20px #3b82f6; }}
    .locked {{ background: #334155; opacity: 0.4; cursor: not-allowed; }}
    .boss {{ background: gold; color: black; }}
    .exam {{ background: purple; }}

    .line {{
        width: 6px;
        height: 40px;
        background: #475569;
    }}
    </style>

    <div class="map">
    """

    for i, lesson in enumerate(lessons):
        cls = "node"

        if lesson["type"] == "boss":
            cls += " boss"
        elif lesson["type"] == "exam":
            cls += " exam"

        if lesson["status"] == "done":
            cls += " done"
        elif lesson["status"] == "current":
            cls += " current"
        else:
            cls += " locked"

        side = "left" if i % 2 == 0 else "right"
        label = lesson.get("label", str(i+1))
        click_js = f"window.parent.postMessage('{unit_id}|{i}', '*')" if lesson["status"] != "locked" else ""

        html += f"""
        <div class="row {side}">
            <div class="{cls}" onclick="{click_js}">
                {label}
            </div>
        </div>
        """

        if i < len(lessons) - 1:
            html += "<div class='line'></div>"

    html += "</div>"

    return components.html(f"""
    {html}
    <script>
    window.addEventListener("message", (event) => {{
        const data = event.data;
        if (data && typeof data === 'string' && data.includes('|')) {{
            window.parent.postMessage({{ type: "streamlit:setComponentValue", value: data }}, "*");
        }}
    }});
    </script>
    """, height=650)

# ================= 5. LOAD/SAVE =================
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
    except Exception as e:
        print("Lỗi lưu tiến trình:", e)

def save_coins():
    if "user" in st.session_state and st.session_state.user:
        try:
            supabase.table("users").upsert({
                "email": st.session_state.user,
                "coins": st.session_state.coins
            }).execute()
        except Exception as e:
            print(f"Lưu coin thất bại: {e}")

# ================= 6. SESSION =================
if "coins" not in st.session_state:
    st.session_state.update({
        "coins": 100,
        "streak": 0,
        "last_login": "",
        "percent": None,
        "lesson_progress": {},
        "current_lesson": None,
        "q_index": 0,
        "chat_history": [],
        "skills": {},
        "learned_lessons": [],
        "daily_learn": 0
    })

# ================= 7. AUTH =================
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
                st.success("Đăng ký xong! Hãy qua tab Đăng nhập.")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    st.stop()

# ================= 8. LOAD PROGRESS =================
if "progress_loaded" not in st.session_state:
    db_progress = load_progress()
    for l_id, data in db_progress.items():
        st.session_state.lesson_progress[l_id] = {
            "answers": {},
            "submitted": True,
            "score": data.get("score", 0)
        }
    st.session_state.progress_loaded = True

# ================= 9. DAILY REWARD =================
today = str(datetime.date.today())
if st.session_state.last_login != today:
    st.session_state.coins += 20
    st.session_state.last_login = today
    save_coins()

# ================= 10. UI =================
coins = st.session_state.coins
rank = "🥉 Intern" if coins < 100 else "🥈 Junior" if coins < 300 else "🥇 Senior" if coins < 600 else "👑 Manager"

st.sidebar.markdown(f"### 🎖️ Rank: {rank}")
st.sidebar.markdown(f"### 💰 Coins: {coins}")

menu = st.sidebar.radio("Menu", [
    "📘 Học", "🎓 Lớp học AI (Quiz)", "🎓 Lớp học AI (Chat)",
    "💼 Đi làm", "🧾 Case Study", "📊 Dashboard",
    "📊 Financial Report", "🤖 Chấm bút toán",
    "📚 Từ điển", "🚨 Fraud Detection", "🏆 Leaderboard"
])

# ================= 11. LEARNING MAP =================
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

        level_name = level.get('level')
        required = level.get("unlock_coins", 0)
        unlocked = st.session_state.coins >= required

        st.markdown(f"## {'🔓' if unlocked else '🔒'} {level_name} (Cần {required} 💰)")

        for module in level.get("modules", []):
            st.markdown(f"### 📚 {module['name']}")

            lesson_nodes = []
            prev_passed = True

            for i, lesson in enumerate(module["lessons"]):
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"

                if l_id not in st.session_state.lesson_progress:
                    st.session_state.lesson_progress[l_id] = {"submitted": False, "score": 0}

                prog = st.session_state.lesson_progress[l_id]

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

            lesson_nodes.append({
                "status": "current" if prev_passed else "locked",
                "type": "boss",
                "label": "👑"
            })

            if module == level["modules"][-1]:
                lesson_nodes.append({
                    "status": "locked",
                    "type": "exam",
                    "label": "🎓"
                })

            clicked = render_duolingo_pro(module["name"], lesson_nodes)

            if clicked:
                unit, index = clicked.split("|")
                if unit == module["name"]:
                    idx = int(index)
                    if idx < len(module["lessons"]):
                        sel = module["lessons"][idx]
                        st.session_state.current_lesson = sel
                        st.session_state.current_lesson_id = f"{level_name}_{module['name']}_{sel['title']}"
                        st.rerun()

# ================= LOGOUT =================
st.sidebar.divider()
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()
