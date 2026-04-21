import streamlit as st
# ===== GLOBAL STATE (ANTI BUG) =====
if "coins" not in st.session_state:
    st.session_state.coins = 100

if "skills" not in st.session_state:
    st.session_state.skills = {}

if "percent" not in st.session_state:
    st.session_state.percent = None

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
from data.question_bank import question_bank
from engine.ai_teacher import teacher_explain
from engine.progress_tracker import update_progress
from engine.classroom_ai import classroom_chat
from data.curriculum import curriculum
from data.dictionary import dictionary
import sys
import os
sys.path.append(os.path.dirname(__file__))

from data.jobs import jobs
from engine.boss_ai import boss_msg
from engine.ai_grader import grade
from data.case_study import case_studies

# ===== CONFIG =====
st.set_page_config(page_title="Phong AI Accounting", layout="wide")
if "dark" not in st.session_state:
    st.session_state.dark = False

dark = st.toggle("🌙 Dark Mode", value=st.session_state.dark)
st.session_state.dark = dark

bg = "#000" if dark else "#f2f2f7"
card = "rgba(28,28,30,0.8)" if dark else "white"

st.markdown(f"""
<style>
body {{background:{bg};}}

.card {{
    background:{card};
    padding:16px;
    border-radius:20px;
    box-shadow:0 4px 15px rgba(0,0,0,0.1);
    margin-bottom:12px;
}}

.stButton>button {{
    width:100%;
    height:50px;
    border-radius:15px;
}}
</style>
""", unsafe_allow_html=True)

# ===== STATE =====
if "coins" not in st.session_state:
    st.session_state.coins = 100

# ===== HEADER =====
st.markdown(f"""
<div class="card">
<h2>📱 Phong AI Accounting</h2>
💰 Coins: {st.session_state.coins}
</div>
""", unsafe_allow_html=True)

if "skills" in st.session_state:
    for skill, data in st.session_state.skills.items():
        total = data["correct"] + data["wrong"]

        if total > 0:
            acc = data["correct"] / total * 100
        else:
            acc = 0

        st.write(f"{skill}: {round(acc,1)}%")

# ===== MENU =====
menu = st.sidebar.radio("Menu", [
    "📘 Học",
    "🎓 Lớp học AI (Quiz)",   # 👈 học chuẩn
    "🎓 Lớp học AI (Chat)",   # 👈 chat realtime
    "💼 Đi làm",
    "🧾 Case Study",
    "📊 Dashboard",
    "📊 Financial Report"
    "🤖 Chấm bút toán",
    "📚 Từ điển"
])


# ================= HỌC =================
if menu == "📘 Học":
    st.write("Phần học cơ bản")

# ================= QUIZ =================
elif menu == "🎓 Lớp học AI (Quiz)":

    st.header("🎓 Lớp học chuẩn giáo dục")

    # ===== INIT =====
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0

    q = question_bank[st.session_state.q_index]

    # ===== UI =====
    st.markdown(f"""
    <div class='card'>
        <b>Câu {q['id']}:</b><br>{q['question']}
    </div>
    """, unsafe_allow_html=True)

    answer = st.radio("Chọn đáp án:", q["options"])

    # ===== SUBMIT =====
    if st.button("🚀 Nộp bài"):

        correct = q["options"].index(answer) == q["correct"]

        update_progress(q["skill"], correct, st.session_state)

        if correct:
            st.success("✅ Đúng +10 coins")
            st.session_state.coins += 10
        else:
            st.error("❌ Sai -5 coins")
            st.session_state.coins -= 5

        st.info(q["explain"])

        if st.button("➡️ Câu tiếp theo"):
            st.session_state.q_index += 1
            st.rerun()

# ================= CHAT AI =================
elif menu == "🎓 Lớp học AI (Chat)":

    st.header("🎓 Lớp học AI (Real-time)")

    # ===== INIT =====
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hôm nay học: Tài sản = ?"}
        ]

    # ===== HIỂN THỊ CHAT =====
    for msg in st.session_state.chat_history:

        if msg["role"] == "user":
            st.markdown(f"""
            <div style='text-align:right; margin:8px;'>
                <span style='background:#007AFF;color:white;
                padding:8px 12px;border-radius:15px;'>
                {msg["content"]}
                </span>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div style='text-align:left; margin:8px;'>
                <span style='background:#E5E5EA;
                padding:8px 12px;border-radius:15px;'>
                {msg["content"]}
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ===== INPUT =====
    user = st.text_input("Nhập câu trả lời hoặc câu hỏi")

    if st.button("Gửi") and user:

        # lưu user
        st.session_state.chat_history.append({
            "role": "user",
            "content": user
        })

        # gọi AI
        with st.spinner("🤖 Giáo viên đang suy nghĩ..."):
            reply = classroom_chat(
                st.session_state.chat_history,
                user
            )

        # lưu AI
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": reply
        })

        # 🎮 GAME HOÁ
        if "đúng" in reply.lower():
            st.session_state.coins += 10
        else:
            st.session_state.coins -= 5

        st.rerun()

    # ===== RESET =====
    if st.button("🔄 Reset lớp học"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Bắt đầu lại: Tài sản = ?"}
        ]
        st.rerun()

# ================= TỪ ĐIỂN =================
elif menu == "📚 Từ điển":

    st.header("📚 Từ điển")

    key = st.text_input("Nhập TK")

    if key in dictionary:
        st.success(dictionary[key])
    elif key != "":
        st.warning("Không tìm thấy")


# ================= ĐI LÀM =================
elif menu == "💼 Đi làm":

    import random

    st.header("🏢 Company Mode - Mô phỏng doanh nghiệp")

    # ===== INIT STATE =====
    if "work_day" not in st.session_state:
        st.session_state.work_day = 1

    if "performance" not in st.session_state:
        st.session_state.performance = 100

    if "role" not in st.session_state:
        st.session_state.role = "Intern"

    if "fail_count" not in st.session_state:
        st.session_state.fail_count = 0

    if "department" not in st.session_state:
        st.session_state.department = "Kế toán tổng hợp"

    # ===== ROLE SYSTEM =====
    if st.session_state.work_day > 25:
        st.session_state.role = "Manager"
    elif st.session_state.work_day > 15:
        st.session_state.role = "Senior"
    elif st.session_state.work_day > 7:
        st.session_state.role = "Junior"
    else:
        st.session_state.role = "Intern"

    # ===== HEADER =====
    st.markdown(f"""
    <div class='card'>
    📅 Day: {st.session_state.work_day}/30<br>
    🧑‍💼 Role: <b>{st.session_state.role}</b><br>
    🏢 Department: {st.session_state.department}<br>
    📊 Performance: {st.session_state.performance}%
    </div>
    """, unsafe_allow_html=True)

    # ===== DEPARTMENT TASK =====
    departments = {
        "Kế toán tổng hợp": jobs[0]["tasks"],
        "Kế toán thuế": jobs[0]["tasks"],
        "Kế toán kho": jobs[0]["tasks"]
    }

    dept = st.selectbox("Chọn phòng ban", list(departments.keys()))
    st.session_state.department = dept

    task = random.choice(departments[dept])

    # ===== DIFFICULTY =====
    difficulty = random.choice(["Easy", "Medium", "Hard"])
    reward = {"Easy": 10, "Medium": 20, "Hard": 30}
    penalty = {"Easy": 5, "Medium": 10, "Hard": 15}

    # ===== EVENT SYSTEM =====
    events = [
        "📄 Sai hóa đơn VAT",
        "💸 Lệch quỹ tiền mặt",
        "📊 Sai báo cáo thuế",
        "🔍 Kiểm tra đột xuất",
        "⚠️ Khách hàng khiếu nại"
    ]

    event = random.choice(events)

    st.warning(f"⚠️ Sự kiện hôm nay: {event}")

    # ===== TASK UI =====
    st.markdown(f"""
    <div class='card'>
    <b>📌 Nhiệm vụ ({difficulty}):</b><br>
    {task['description']}
    </div>
    """, unsafe_allow_html=True)

    st.metric("💰 Lương task", f"+{reward[difficulty]} coins")

    # ===== BOSS =====
    try:
        st.info("👨‍💼 Boss: " + boss_msg(task))
    except:
        st.warning("Boss offline")

    # ===== INPUT =====
    user = st.text_input("✍️ Nhập bút toán")

    # ===== SUBMIT =====
    if st.button("🚀 Nộp task"):

        if user.strip() == "":
            st.warning("Bạn chưa nhập")
        else:

            if user.lower() in task["correct"].lower():

                st.success(f"✅ Đúng +{reward[difficulty]} coins")

                st.session_state.coins += reward[difficulty]
                st.session_state.performance += 2
                st.session_state.fail_count = 0

            else:
                st.error(f"❌ Sai -{penalty[difficulty]} coins")

                st.session_state.coins -= penalty[difficulty]
                st.session_state.performance -= 5
                st.session_state.fail_count += 1

                # AI HINT
                try:
                    hint = teacher_explain(task["description"], user)
                    st.info("🤖 Gợi ý:")
                    st.write(hint)
                except:
                    st.info("💡 Kiểm tra lại Nợ/Có")

        # ===== DAY UP =====
        st.session_state.work_day += 1

    # ===== AUDIT SYSTEM =====
    if st.session_state.fail_count >= 3:
        st.error("🚨 BỊ KIỂM TOÁN!")
        st.session_state.performance -= 10
        st.session_state.fail_count = 0

    # ===== KPI =====
    st.progress(st.session_state.performance / 100)

    # ===== END GAME =====
    if st.session_state.work_day > 30:

        st.success("🎉 Hoàn thành 30 ngày làm việc!")

        if st.session_state.performance > 85:
            st.success("🏆 Xuất sắc - Sẵn sàng đi làm thật")
        elif st.session_state.performance > 65:
            st.info("👍 Khá - Có thể làm việc")
        else:
            st.error("⚠️ Cần đào tạo lại")

        st.stop()

    # ===== RESET =====
    if st.button("🔄 Reset Company"):
        st.session_state.work_day = 1
        st.session_state.performance = 100
        st.session_state.fail_count = 0
        st.session_state.coins = 100
        st.rerun()
elif menu == "📊 Dashboard":

    st.header("📊 Phân tích học lực")

    if "skills" in st.session_state:

        total_correct = sum(v["correct"] for v in st.session_state.skills.values())
        total_wrong = sum(v["wrong"] for v in st.session_state.skills.values())

        acc = total_correct / (total_correct + total_wrong) * 100 if (total_correct+total_wrong)>0 else 0

        st.metric("🎯 Accuracy", f"{round(acc,1)}%")
        st.metric("✅ Đúng", total_correct)
        st.metric("❌ Sai", total_wrong)

        # Rank giả lập
        if acc > 80:
            st.success("🏆 Rank: Expert")
        elif acc > 60:
            st.info("🥈 Rank: Intermediate")
        else:
            st.warning("🥉 Rank: Beginner")
elif menu == "🧾 Case Study":

    st.header("🧾 Case Study - Tháng 1")

    case = case_studies[0]

    score = 0

    for i, trans in enumerate(case["transactions"]):
        st.write(f"{i+1}. {trans}")
        ans = st.text_input("Định khoản", key=f"case_{i}")

        if ans.lower() in case["answers"][i].lower():
            score += 1

    if st.button("Chấm Case"):
        st.write(f"Điểm: {score}/{len(case['answers'])}")
elif menu == "🏆 Thi":

    st.header("🏆 Thi cuối khóa")

    exam = exams[0]

    # ===== HIỂN THỊ =====
percent = st.session_state.get("percent", None)

if percent is not None:

    percent = float(percent)

    st.success(f"🎯 Điểm: {round(percent,1)}%")
    st.progress(percent / 100)

    if percent >= 70:
        st.balloons()
        st.success("🎓 ĐẬU!")
    else:
        st.error("❌ RỚT!")
    answers = []

    for i, q in enumerate(exam["questions"]):
        ans = st.radio(q["question"], q["options"], key=f"exam_{i}")
        answers.append(ans)

    if st.button("Nộp bài thi"):

        score = 0

        for i, q in enumerate(exam["questions"]):
            if q["options"].index(answers[i]) == q["correct"]:
                score += 1

        st.session_state.percent = score / len(exam["questions"]) * 100

    # ===== HIỂN THỊ =====
    percent = st.session_state.get("percent", None)

    if percent is not None:

        st.success(f"🎯 Điểm: {round(percent,1)}%")
        st.progress(percent / 100)

        if percent >= 70:
            st.balloons()
            st.success("🎓 ĐẬU!")
        else:
            st.error("❌ RỚT!")
if percent >= 70:
    st.success("🎓 CHỨNG NHẬN HOÀN THÀNH")
    st.download_button(
        "📥 Tải chứng nhận",
        "Phong AI Accounting Certificate",
        file_name="certificate.txt"
    )


# ================= AI GRADER =================
elif menu == "🤖 Chấm bút toán":

    entry = st.text_area("Nhập bút toán")

    if st.button("Chấm"):
        st.write(grade(entry))
