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

# ===== CONFIG =====
st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ===== STATE =====
if "coins" not in st.session_state:
    st.session_state.coins = 100

# ===== HEADER =====
st.title("🚀 PHONG AI ACCOUNTING")

st.metric("💰 Coins", st.session_state.coins)

# ===== MENU =====
menu = st.sidebar.radio("Menu", [
    "📘 Học",
    "🎓 Lớp học AI (Quiz)",   # 👈 học chuẩn
    "🎓 Lớp học AI (Chat)",   # 👈 chat realtime
    "💼 Đi làm",
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


# ================= AI GRADER =================
elif menu == "🤖 Chấm bút toán":

    entry = st.text_area("Nhập bút toán")

    if st.button("Chấm"):
        st.write(grade(entry))
