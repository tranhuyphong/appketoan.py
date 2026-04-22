import streamlit as st
import random
import datetime
import streamlit.components.v1 as components

def render_unit_map(module_name, lessons):

    html = f"""
    <style>
    .unit {
        background: #0f172a;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 30px;
    }

    .unit-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .lesson-row {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
    }

    .node {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        cursor: pointer;
        transition: 0.2s;
    }

    .node:hover {
        transform: scale(1.1);
    }

    .done { background: #22c55e; }
    .current { background: #3b82f6; }
    .locked { background: #475569; opacity: 0.4; }

    </style>

    <div class="unit">
        <div class="unit-title">{module_name}</div>
        <div class="lesson-row">
    """

    for i, lesson in enumerate(lessons):

        if lesson["status"] == "done":
            cls = "node done"
        elif lesson["status"] == "current":
            cls = "node current"
        else:
            cls = "node locked"

        html += f"<div class='{cls}'>{i+1}</div>"

    html += "</div></div>"

    components.html(html, height=200)
# ================= SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indqd3Rvd21kY2RrcHJ5eGNxcXR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3NjY1NDMsImV4cCI6MjA5MjM0MjU0M30.jX4wAiXNezvmnwvr1hucjRxANZ5jWgzwn_9BsVCoueg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= INIT STATE =================
def init_state():
    defaults = {
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
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ================= LOGIN / REGISTER =================
if "user" not in st.session_state:
    st.title("🚀 PHONG AI ACCOUNTING")
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký tài khoản"])

    with tab1:
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_pw")
        
        if st.button("Đăng nhập"):
            try:
                res = supabase.auth.sign_in_with_password({
                    "email": login_email,
                    "password": login_password
                })
                if res.user:
                    st.session_state.user = res.user.email
                    st.success("Đăng nhập thành công!")
                    st.rerun()
            except Exception as e:
                st.error("Sai tài khoản hoặc mật khẩu!")
    with tab2:
        reg_email = st.text_input("Email đăng ký", key="reg_email")
        reg_password = st.text_input("Password đăng ký", type="password", key="reg_pw")
        confirm_password = st.text_input("Xác nhận Password", type="password", key="reg_pw_conf")
        
        if st.button("Thực hiện Đăng ký"):
            if reg_password != confirm_password:
                st.warning("Mật khẩu xác nhận không khớp!")
            elif len(reg_password) < 6:
                st.warning("Mật khẩu phải có ít nhất 6 ký tự!")
            else:
                try:
                    supabase.auth.sign_up({
                        "email": reg_email,
                        "password": reg_password
                    })
                    st.success("Tạo tài khoản thành công! Vui lòng kiểm tra email (nếu cần) và qua tab Đăng nhập.")
                except Exception as e:
                    st.error(f"Lỗi: {e}")

    st.stop()

# ================= PROGRESS SYSTEM =================
def load_progress():
    try:
        res = supabase.table("users_progress")\
            .select("*")\
            .eq("email", st.session_state.user)\
            .execute()
        return {r["lesson_id"]: r for r in res.data}
    except:
        return {}

if "progress_loaded" not in st.session_state:
    db_progress = load_progress()
    for lesson_id, data in db_progress.items():
        st.session_state.lesson_progress[lesson_id] = {
            "answers": {},
            "submitted": True,
            "score": data.get("score", 0)
        }
    st.session_state.progress_loaded = True

# ================= SAVE =================
def save_coins():
    if "user" in st.session_state and st.session_state.user:
        try:
            supabase.table("users").upsert({
                "email": st.session_state.user,
                "coins": st.session_state.coins
            }).execute()
        except Exception as e:
            print(f"Lưu coin thất bại: {e}")

# ================= DAILY =================
if "user" in st.session_state: 
    today = str(datetime.date.today())
    
    if st.session_state.last_login != today:
        st.session_state.coins += 20
        st.session_state.last_login = today
        st.success("🎁 Daily +20 coins")
        save_coins()
    
    if st.session_state.daily_learn >= 3:
        st.success("🎁 Daily học đủ 3 bài +30 coins")
        st.session_state.coins += 30
        st.session_state.daily_learn = 0 
        save_coins()

# ================= IMPORT MODULE =================
from data.question_bank import question_bank
from engine.ai_teacher import teacher_explain
from engine.progress_tracker import update_progress
from engine.classroom_ai import classroom_chat
from data.curriculum import curriculum
from data.dictionary import dictionary
from data.jobs import jobs
from engine.boss_ai import boss_msg
from engine.ai_grader import grade
from data.case_study import case_studies

# ================= CONFIG =================
st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ================= HEADER =================
coins = st.session_state.coins

if coins < 100:
    rank = "🥉 Intern"
elif coins < 300:
    rank = "🥈 Junior"
elif coins < 600:
    rank = "🥇 Senior"
else:
    rank = "👑 Manager"

st.markdown(f"""
<div style='padding:20px;background:#1e293b;border-radius:20px'>
<h2>📱 Phong AI Accounting</h2>
💰 {coins} | 🔥 {st.session_state.streak} | 🎖 {rank}
</div>
""", unsafe_allow_html=True)
st.write(f"🔥 Streak học: {st.session_state.streak}")

# ================= PROGRESS SYSTEM (RE-DEFINED FOR SCOPE) =================
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
        print("Save progress error:", e)

# ================= MENU =================
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

# ================= HỌC =================
if menu == "📘 Học":
    st.header("🗺️ Learning Map")
    for level in learning_path:
        required = level.get("unlock_coins", 0)
        unlocked = st.session_state.coins >= required

        if unlocked:
            st.markdown(f"## 🔓 {level['level']}")
        else:
            st.markdown(f"## 🔒 {level['level']} (Cần {required} 💰)")
            st.warning("💰 Chưa đủ coin")
            continue

        for module in level["modules"]:
            st.markdown(f"### 📚 {module['name']}")
            lesson_nodes = []
            prev_passed = True  

            for lesson in module["lessons"]:
                lesson_id = f"{level['level']}_{module['name']}_{lesson['title']}"
                if lesson_id not in st.session_state.lesson_progress:
                    st.session_state.lesson_progress[lesson_id] = {
                        "answers": {},
                        "submitted": False,
                        "score": 0
                    }
                state = st.session_state.lesson_progress[lesson_id]
                if state["submitted"] and state["score"] >= 70:
                    status = "done"
                elif prev_passed:
                    status = "current"
                else:
                    status = "locked"
                lesson_nodes.append({"status": status})
                prev_passed = state["submitted"] and state["score"] >= 70

            render_unit_map(module["name"], lesson_nodes)

            prev_passed = True  
            for lesson in module["lessons"]:
                lesson_id = f"{level['level']}_{module['name']}_{lesson['title']}"
                lesson_state = st.session_state.lesson_progress[lesson_id]
                unlocked = prev_passed
                if lesson_state["submitted"]:
                    icon = "✅" if lesson_state["score"] >= 70 else "❌"
                elif unlocked:
                    icon = "⬜"
                else:
                    icon = "🔒"

                with st.expander(f"{icon} {lesson['title']}"):
                    if not unlocked:
                        st.warning("🔒 Hoàn thành bài trước để mở khóa")
                        continue
                    st.write(lesson["content"])
                    st.divider()
                    correct_count = 0
                    for i, q in enumerate(lesson["quiz"]):
                        ans = st.radio(
                            q["question"],
                            q["options"],
                            key=f"{lesson_id}_{i}",
                            disabled=lesson_state["submitted"]
                        )
                        lesson_state["answers"][i] = ans
                        if ans == q["options"][q["answer"]]:
                            correct_count += 1

                    if not lesson_state["submitted"]:
                        if st.button("🚀 Nộp bài", key=f"submit_{lesson_id}"):
                            score = int((correct_count / len(lesson["quiz"])) * 100)
                            lesson_state["submitted"] = True
                            lesson_state["score"] = score
                            if score >= 70:
                                st.success(f"🎉 Pass {score}%")
                                save_progress(lesson_id, score)
                                reward = lesson.get("xp", 20)
                                st.session_state.coins += reward
                                st.session_state.daily_learn += 1
                                st.success(f"💰 +{reward} coins")
                            else:
                                st.error(f"❌ Fail {score}%")
                            save_coins()
                            st.rerun()
                    else:
                        if lesson_state["score"] >= 70:
                            st.success(f"✅ Hoàn thành ({lesson_state['score']}%)")
                        else:
                            st.error(f"❌ Chưa đạt ({lesson_state['score']}%)")
                prev_passed = lesson_state["submitted"] and lesson_state["score"] >= 70

# ================= PHẦN CÒN LẠI GIỮ NGUYÊN (QUIZ, CHAT, ĐI LÀM, ETC.) =================
elif menu == "🎓 Lớp học AI (Quiz)":
    q = question_bank[st.session_state.q_index]
    st.subheader(q["question"])
    answer = st.radio("Chọn:", q["options"])
    if st.button("Nộp bài"):
        correct = q["options"].index(answer) == q["correct"]
        update_progress(q["skill"], correct, st.session_state)
        if correct:
            st.session_state.streak += 1
            reward = min(10 + st.session_state.streak * 2, 30)
            st.success(f"✅ +{reward} 🔥 x{st.session_state.streak}")
            st.session_state.coins += reward
        else:
            st.session_state.streak = 0
            st.error("❌ -5")
            st.session_state.coins -= 5
        st.info(q["explain"])
        save_coins()
    if st.button("➡️ Câu tiếp"):
        st.session_state.q_index += 1
        st.rerun()

elif menu == "🎓 Lớp học AI (Chat)":
    if len(st.session_state.chat_history) == 0:
        st.session_state.chat_history = [{"role": "assistant", "content": "Tài sản = ?"}]
    for msg in st.session_state.chat_history:
        st.write(msg["content"])
    user = st.text_input("Nhập")
    if st.button("Gửi") and user:
        st.session_state.chat_history.append({"role": "user", "content": user})
        reply = classroom_chat(st.session_state.chat_history, user)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        if "đúng" in reply.lower():
            st.session_state.coins += 10
        else:
            st.session_state.coins -= 5
        save_coins()
        st.rerun()

elif menu == "💼 Đi làm":
    st.header("🏢 Career Mode - Real Accountant Life")
    if "work_day" not in st.session_state: st.session_state.work_day = 1
    if "performance" not in st.session_state: st.session_state.performance = 100
    if "fail" not in st.session_state: st.session_state.fail = 0
    if "stress" not in st.session_state: st.session_state.stress = 0

    st.markdown(f"""
    <div style='padding:15px;background:#0f172a;border-radius:15px'>
    📅 Day {st.session_state.work_day}/30  👔 Role: {rank}  📊 KPI: {st.session_state.performance}%  😵 Stress: {st.session_state.stress}  💰 Coins: {st.session_state.coins}
    </div>
    """, unsafe_allow_html=True)
    
    role_key = rank.split(" ")[1] if " " in rank else rank
    task = random.choice(career_tasks.get(role_key, career_tasks["Intern"]))
    st.subheader("📌 Nhiệm vụ")
    st.write(task["desc"])
    options = [task["correct"]] + random.sample(task["wrong"], len(task["wrong"]))
    random.shuffle(options)
    choice = st.radio("Bạn xử lý:", options)

    if st.button("🚀 Xử lý"):
        if choice == task["correct"]:
            reward = random.randint(15, 40)
            st.success(f"✅ Đúng +{reward}")
            st.session_state.coins += reward
            st.session_state.performance += 3
        else:
            st.error("❌ Sai!")
            st.session_state.coins -= 15
            st.session_state.performance -= 7
            st.session_state.stress += 10
            st.session_state.fail += 1
        st.session_state.work_day += 1
        save_coins()
    st.progress(st.session_state.performance / 100 if st.session_state.performance <= 100 else 1.0)

elif menu == "🧾 Case Study":
    case = case_studies[0]
    answers = []
    for i, t in enumerate(case["transactions"]):
        st.write(t)
        answers.append(st.text_input(f"Case {i}", key=f"case_{i}"))
    if st.button("Chấm"):
        score = 0
        for i in range(len(case["answers"])):
            if answers[i].lower() in case["answers"][i].lower(): score += 1
        percent = score / len(case["answers"]) * 100
        st.session_state.percent = percent
        st.success(f"{round(percent,1)}%")
        if percent >= 70:
            st.success("🎓 ĐẬU")
            st.session_state.coins += int(percent)
        else: st.error("❌ RỚT")
        save_coins()

elif menu == "📊 Dashboard":
    st.metric("Coins", st.session_state.coins)
    st.metric("Streak", st.session_state.streak)
    st.metric("Rank", rank)

elif menu == "📊 Financial Report":
    from data.finance_data import transactions
    from engine.financial_report import generate_report
    import pandas as pd
    report = generate_report(transactions)
    st.metric("Doanh thu", report["revenue"])
    st.metric("Chi phí", report["expense"])
    st.metric("Lợi nhuận", report["profit"])
    st.dataframe(pd.DataFrame(transactions))

elif menu == "🚨 Fraud Detection":
    from data.finance_data import transactions
    from engine.fraud_detection import detect_fraud
    alerts = detect_fraud(transactions)
    if len(alerts) == 0: st.success("Không có gian lận")
    else:
        for a in alerts: st.error(a)

elif menu == "📚 Từ điển":
    key = st.text_input("Nhập TK")
    if key in dictionary: st.success(dictionary[key])

elif menu == "🤖 Chấm bút toán":
    entry = st.text_area("Nhập")
    if st.button("Chấm"): st.write(grade(entry))

elif menu == "🏆 Leaderboard":
    res = supabase.table("users").select("*").order("coins", desc=True).limit(10).execute()
    for i, u in enumerate(res.data):
        st.write(f"{i+1}. {u['email']} - {u['coins']}")
