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
    from data.job_tasks import job_tasks
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
# ================= TIMER REALTIME =================
import streamlit.components.v1 as components

def realtime_timer(duration, key):
    if key not in st.session_state or st.session_state[key] is None:
        st.session_state[key] = int(time.time())

    js = f"""
    <script>
    let start = {st.session_state[key]};
    let duration = {duration};

    function updateTimer(){{
        let now = Math.floor(Date.now()/1000);
        let remaining = duration - (now - start);

        if(remaining < 0) remaining = 0;

        document.getElementById("{key}").innerText = "⏱ " + remaining + "s";

        if(remaining <= 0){{
            window.parent.postMessage({{type: "streamlit:rerun"}}, "*");
        }}
    }}

    setInterval(updateTimer, 1000);
    </script>
    <div id="{key}">⏱ {duration}s</div>
    """

    components.html(js, height=40)

    remaining = duration - (int(time.time()) - st.session_state[key])
    return max(remaining, 0)

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
def update_level():
    xp = st.session_state.xp
    st.session_state.level = xp // 100 + 1
def update_role():
    lvl = st.session_state.level

    if lvl >= 10:
        st.session_state.role = "Manager"
        st.session_state.salary = 500
    elif lvl >= 7:
        st.session_state.role = "Senior"
        st.session_state.salary = 300
    elif lvl >= 4:
        st.session_state.role = "Staff"
        st.session_state.salary = 200
    else:
        st.session_state.role = "Intern"
        st.session_state.salary = 100

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
if "xp" not in st.session_state:
    st.session_state.xp = 0

if "level" not in st.session_state:
    st.session_state.level = 1
if "bank" not in st.session_state:
    st.session_state.bank = 0
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = True  # bật test
if st.session_state.get("dev_mode"):
    st.session_state.coins = 9999
    st.session_state.xp = 999
    st.session_state.salary = 500
# ===== JOB SYSTEM =====
if "job_mode" not in st.session_state:
    st.session_state.job_mode = False

if "job_task" not in st.session_state:
    st.session_state.job_task = None

if "job_done_today" not in st.session_state:
    st.session_state.job_done_today = 0

if "last_job_date" not in st.session_state:
    st.session_state.last_job_date = str(datetime.date.today())

if "correct_job" not in st.session_state:
    st.session_state.correct_job = 0

if "total_job" not in st.session_state:
    st.session_state.total_job = 0

if "salary" not in st.session_state:
    st.session_state.salary = 100

if "role" not in st.session_state:
    st.session_state.role = "Intern"

# ===== Boss state =====
if "boss_mode" not in st.session_state:
    st.session_state.boss_mode = False

if "boss_chat" not in st.session_state:
    st.session_state.boss_chat = []

if "boss_turn" not in st.session_state:
    st.session_state.boss_turn = 0

if "boss_score" not in st.session_state:
    st.session_state.boss_score = 0

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
st.sidebar.markdown(f"💰 Coins: {st.session_state.coins}")
st.sidebar.markdown(f"⭐ XP: {st.session_state.xp}")
st.sidebar.markdown(f"🏆 Level: {st.session_state.level}")
st.sidebar.markdown(f"🧑‍💼 Role: {st.session_state.role}")
st.sidebar.markdown(f"🏦 Bank: {st.session_state.bank}")
st.sidebar.markdown(f"💼 Salary/month: {st.session_state.salary}")

menu_options = [
    "📘 Học",
    "🎓 Lớp học AI (Quiz)",
    "🎓 Lớp học AI (Chat)"
]

# 🔒 unlock khi level >= 3
menu_options.append("💼 Đi làm")

menu_options += [
    "🧾 Case Study",
    "📊 Dashboard",
    "📊 Financial Report",
    "🤖 Chấm bút toán",
    "📚 Từ điển",
    "🚨 Fraud Detection",
    "🏆 Leaderboard",
    "🎓 Chứng chỉ",
]

menu = st.sidebar.radio("Menu", menu_options)

# ================= 📘 LEARNING =================
import time

if menu == "📘 Học":
    st.header("🗺️ Learning Map")

    # ================= LESSON =================
    if st.session_state.current_lesson:
        lesson = st.session_state.current_lesson
        l_id = st.session_state.current_lesson_id

        st.success(f"📖 {lesson['title']}")

        remaining = realtime_timer(20, "lesson_timer")

        if remaining > 0 and not st.session_state.get("start_quiz", False):
            st.write(lesson["content"])

            if st.button("👉 Làm quiz"):
                st.session_state.start_quiz = True
                st.rerun()

        else:
            st.warning("🧠 Quiz")

            questions = lesson.get("quiz", [])
            if not questions:
                st.info("Chưa có quiz")
                st.stop()

            if "quiz_index" not in st.session_state:
                st.session_state.quiz_index = 0
                st.session_state.correct = 0

            i = st.session_state.quiz_index

            if i < len(questions):
                q = questions[i]

                st.write(f"### ❓ {q['question']}")
                ans = st.radio("Chọn", q["options"], key=f"{l_id}_{i}")

                if st.button("👉 Trả lời"):
                    if q["options"].index(ans) == q["answer"]:
                        st.session_state.correct += 1

                    st.session_state.quiz_index += 1
                    st.rerun()

            else:
                score = int(st.session_state.correct / len(questions) * 100)

                if score >= 70:
                    st.success(f"🎉 PASS {score}% (+20 coins +20 XP)")
                    st.session_state.coins += 20
                    st.session_state.xp += 20
                    update_level()
                    st.session_state.lesson_progress[l_id] = {"score": score}
                else:
                    st.error(f"❌ FAIL {score}%")

                if st.button("🔙 Quay lại"):
                    st.session_state.current_lesson = None
                    st.session_state.quiz_index = 0
                    st.session_state.correct = 0
                    st.session_state.start_quiz = False
                    st.session_state.lesson_timer = None
                    st.rerun()

    # ================= MAP =================
    for level_index, level in enumerate(curriculum):
        level_name = level.get("level", "Level")

        if level_index == 0:
            unlocked = True
        else:
            prev = curriculum[level_index - 1]
            exam_id_prev = f"{prev['level']}_{prev['modules'][-1]['name']}_exam"
            unlocked = st.session_state.lesson_progress.get(exam_id_prev, {}).get("score", 0) >= 70

        st.markdown(f"## {'🔓' if unlocked else '🔒'} {level_name}")

        for module in level["modules"]:
            st.markdown(f"### 📚 {module['name']}")

            lessons = module["lessons"]
            cols = st.columns(5)

            # ===== LESSON =====
            for i, lesson in enumerate(lessons):
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"

                prog = st.session_state.lesson_progress.get(l_id, {})
                done = prog.get("score", 0) >= 70

                icon = "🟢" if done else "🔵" if unlocked else "⚫"

                with cols[i % 5]:
                    if st.button(icon, key=l_id, disabled=not unlocked):
                        st.session_state.current_lesson = lesson
                        st.session_state.current_lesson_id = l_id
                        st.session_state.lesson_timer = None
                        st.session_state.start_quiz = False
                        st.session_state.quiz_index = 0
                        st.session_state.correct = 0
                        st.rerun()

            # ===== BOSS =====
            boss_id = f"{level_name}_{module['name']}_boss"

            if st.button("👑 Boss", key=boss_id, disabled=not unlocked):
                if len(question_bank) < 5:
                    st.error("❌ Không đủ câu hỏi")
                else:
                    st.session_state.boss_mode = True
                    st.session_state.current_lesson = None
                    st.session_state.boss_q = random.sample(question_bank, 5)
                    st.session_state.boss_i = 0
                    st.session_state.boss_score = 0

            # ===== EXAM =====
            exam_id = f"{level_name}_{module['name']}_exam"
            
            if st.button("🎓 Exam", key=exam_id, disabled=not unlocked):
                st.session_state.exam_mode = True
                st.session_state.exam_q = random.sample(
                    question_bank,
                    min(10, len(question_bank))
                )
                st.session_state.exam_i = 0
                st.session_state.exam_score = 0
                st.session_state.exam_timer = None
            
            # ✅ FIX Ở ĐÂY
            if st.session_state.get("exam_mode") and st.session_state.get("exam_q"):
            
                remaining = realtime_timer(60, "exam_timer")
            
                qs = st.session_state.exam_q
                i = st.session_state.exam_i
            
                if remaining == 0:
                    st.error("⏰ Hết giờ!")
                    i = len(qs)
            
                if i < len(qs):
                    q = qs[i]
            
                    st.write(f"🎓 {q['question']}")
                    ans = st.radio(
                        "Chọn",
                        q["options"],
                        key=f"exam_{i}"
                    )
            
                    if st.button("👉 Trả lời"):
                        if q["options"].index(ans) == q["correct"]:
                            st.session_state.exam_score += 1
            
                        st.session_state.exam_i += 1
                        st.rerun()
            
                else:
                    percent = int(st.session_state.exam_score / len(qs) * 100)
            
                    if percent >= 70:
                        st.success(f"PASS {percent}% (+100 coins)")
                        st.session_state.coins += 100
                        st.session_state.xp += 100
                        update_level()
                        st.session_state.lesson_progress[exam_id] = {"score": percent}
                    else:
                        st.error(f"FAIL {percent}%")
            
                    if st.button("🔁 Thi lại"):
                        st.session_state.exam_mode = False
                        st.rerun()
# ================= BOSS PLAY =================
if st.session_state.get("boss_mode") and st.session_state.get("boss_q"):

    qs = st.session_state.boss_q
    i = st.session_state.boss_i

    if i < len(qs):
        q = qs[i]

        st.write(f"👑 {q['question']}")

        ans = st.radio(
            "Chọn",
            q["options"],
            key=f"boss_{i}"
        )

        if st.button("👉 Trả lời Boss"):
            if q["options"].index(ans) == q["correct"]:
                st.session_state.boss_score += 1

            st.session_state.boss_i += 1
            st.rerun()

    else:
        percent = int(st.session_state.boss_score / len(qs) * 100)

        if percent >= 70:
            st.success(f"👑 Boss PASS {percent}% (+50 coins)")
            st.session_state.coins += 50
            st.session_state.xp += 50
            update_level()
        else:
            st.error(f"💀 Boss FAIL {percent}%")

        if st.button("🔄 Làm lại Boss"):
            st.session_state.boss_mode = False
            st.session_state.boss_q = None
            st.session_state.boss_i = 0
            st.session_state.boss_score = 0
            st.rerun()
# ================= CÁC MENU KHÁC GIỮ NGUYÊN =================
elif menu == "🎓 Lớp học AI (Quiz)":
    st.write("Quiz")

elif menu == "🎓 Lớp học AI (Chat)":
    st.write("Chat")

elif menu == "💼 Đi làm":

    st.header("💼 Đi làm kế toán")

    today = str(datetime.date.today())

    # ===== 💰 LƯƠNG =====
    if "last_salary_day" not in st.session_state:
        st.session_state.last_salary_day = today

    if st.session_state.last_salary_day != today:
        st.session_state.bank += st.session_state.salary
        st.success(f"💰 Nhận lương: +{st.session_state.salary}")
        st.session_state.last_salary_day = today

    # ===== RESET NGÀY =====
    if st.session_state.last_job_date != today:
        st.session_state.job_done_today = 0
        st.session_state.last_job_date = today
        st.session_state.daily_tasks = None

    # ===== KPI =====
    accuracy = 0
    if st.session_state.total_job > 0:
        accuracy = int(
            st.session_state.correct_job / st.session_state.total_job * 100
        )

    st.info(f"""
📊 KPI:
- Accuracy: {accuracy}%
- Jobs hôm nay: {st.session_state.job_done_today}/3
""")

    # ===== 😈 SA THẢI =====
    if st.session_state.total_job >= 5 and accuracy < 50:
        st.error("😈 Bạn bị sa thải do KPI quá thấp!")

        st.session_state.role = "Intern"
        st.session_state.salary = 50
        st.session_state.bank = 0

        st.session_state.total_job = 0
        st.session_state.correct_job = 0

        st.stop()

    # ===== GIỚI HẠN JOB =====
    if st.session_state.job_done_today >= 3:
        st.warning("📅 Hết job hôm nay rồi!")
        st.stop()

    # ===== TẠO TASK THEO NGÀY =====
    if "daily_tasks" not in st.session_state or st.session_state.daily_tasks is None:

        available_tasks = [
            t for t in job_tasks
            if t["level"] <= st.session_state.level
            and t["level"] >= st.session_state.level - 2
        ]

        st.session_state.daily_tasks = random.sample(
            available_tasks,
            min(3, len(available_tasks))
        )

    # ===== NHẬN JOB =====
    if not st.session_state.job_mode:
        if st.button("📋 Nhận việc"):
            st.session_state.job_task = st.session_state.daily_tasks[
                st.session_state.job_done_today
            ]
            st.session_state.job_mode = True
            st.session_state.job_timer = None
            st.rerun()

    # ===== LÀM JOB =====
    if st.session_state.job_mode and st.session_state.job_task:

        task = st.session_state.job_task

        st.subheader(f"{task['title']} ({task['department']})")

        remaining = realtime_timer(task["time"], "job_timer")

        if remaining == 0:
            st.error("⏰ Trễ deadline!")
            st.session_state.coins += task["penalty"]
            st.session_state.job_mode = False
            st.rerun()

        if task.get("type") == "case":
            st.warning("📂 CASE THỰC TẾ")

        st.write(task["question"])

        ans = st.radio("Chọn", task["options"], key="job")

        if st.button("✅ Nộp"):
            st.session_state.total_job += 1
            st.session_state.job_done_today += 1

            if task["options"].index(ans) == task["correct"]:
                st.success("🎉 Đúng!")
                st.session_state.coins += task["salary"]
                st.session_state.xp += task["salary"]
                st.session_state.correct_job += 1
            else:
                st.error("❌ Sai!")
                st.session_state.coins += task["penalty"]

            update_level()
            update_role()

            st.session_state.job_mode = False
            st.rerun()
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
elif menu == "🎓 Chứng chỉ":
    st.header("🎓 Mua chứng chỉ tốt nghiệp")

    st.write("💰 Giá: 200 coins")

    if st.session_state.coins >= 200:
        if st.button("🎓 Mua chứng chỉ"):
            st.session_state.coins -= 200
            st.success("🏆 Bạn đã nhận chứng chỉ kế toán!")
    else:
        st.error("❌ Không đủ coins")

# ================= LOGOUT =================
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()
