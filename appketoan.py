import streamlit as st
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

# ===== STATE =====
if "coins" not in st.session_state:
    st.session_state.coins = 100

# ===== HEADER =====
st.title("🚀 PHONG AI ACCOUNTING")

st.metric("💰 Coins", st.session_state.coins)
st.subheader("📊 Học lực")

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
    "🤖 Chấm bút toán",
    "📚 Từ điển"
])


# ================= HỌC =================
if menu == "📘 Học":
    st.write("Phần học cơ bản")

# ================= QUIZ =================
elif menu == "🎓 Lớp học AI (Quiz)":

    st.header("🎓 Lớp học chuẩn giáo dục")

    if "q_index" not in st.session_state:
        st.session_state.q_index = 0

    q = question_bank[st.session_state.q_index]

    st.subheader(f"Câu hỏi {q['id']}")
    st.write(q["question"])

    answer = st.radio("Chọn đáp án:", q["options"])

    if st.button("Nộp bài"):

        correct = q["options"].index(answer) == q["correct"]

        update_progress(q["skill"], correct, st.session_state)

        if correct:
            st.success("✅ Đúng +10 coins")
            st.session_state.coins += 10

            st.info(q["explain"])

            if st.button("Câu tiếp"):
                st.session_state.q_index += 1
                st.rerun()

        else:
            st.error("❌ Sai -5 coins")
            st.session_state.coins -= 5

            hint = teacher_explain(q["question"], answer)
            st.warning("🤖 Gợi ý:")
            st.write(hint)


# ================= CHAT AI =================
elif menu == "🎓 Lớp học AI (Chat)":

    st.header("🎓 Lớp học AI (Real-time)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hôm nay học phương trình kế toán.\n\n❓ Tài sản = ?"
            }
        ]

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"🧑‍🎓 **Bạn:** {msg['content']}")
        else:
            st.markdown(f"👨‍🏫 **Giáo viên:** {msg['content']}")

    st.divider()

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Nhập câu trả lời")
        submit = st.form_submit_button("Gửi")

    if submit and user_input.strip() != "":
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        reply = classroom_chat(
            st.session_state.chat_history,
            user_input
        )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": reply
        })

        if "đúng" in reply.lower():
            st.session_state.coins += 10
        else:
            st.session_state.coins -= 5

        st.rerun()

    if st.button("🔄 Reset"):
        st.session_state.chat_history = []
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

    task = jobs[0]["tasks"][0]

    st.subheader("Công việc hôm nay")
    st.info(boss_msg(task))

    user = st.text_input("Nhập bút toán")

    if st.button("Nộp task"):
        if user.lower() in task["correct"].lower():
            st.success("+20 coins")
            st.session_state.coins += 20
        else:
            st.error("-10 coins")
            st.session_state.coins -= 10
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

    if "exam_answers" not in st.session_state:
        st.session_state.exam_answers = []

    answers = []

    for i, q in enumerate(exam["questions"]):
        ans = st.radio(q["question"], q["options"], key=f"exam_{i}")
        answers.append(ans)

    if "percent" not in st.session_state:
    st.session_state.percent = None

if st.button("Nộp bài thi"):

    score = 0

    for i, q in enumerate(exam["questions"]):
        if q["options"].index(answers[i]) == q["correct"]:
            score += 1

    st.session_state.percent = score / len(exam["questions"]) * 100

# 👉 dùng ở ngoài OK
if st.session_state.percent is not None:

    percent = st.session_state.percent

    st.write(f"Điểm: {percent}%")

    if percent >= 70:
        st.success("🎓 ĐẬU")
    else:
        st.error("❌ RỚT")
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
