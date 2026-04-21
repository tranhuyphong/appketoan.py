import streamlit as st
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
    "💼 Đi làm",
    "🤖 Chấm bút toán",
    "📚 Từ điển"
    "🎓 Lớp học AI",
])

# ================= HỌC =================
if menu == "📘 Học":
    lesson = curriculum[0]["units"][0]["lessons"][0]

    st.subheader("Bài học")
    st.info(lesson["theory"])

    ans = st.radio(lesson["question"], lesson["options"])

    if st.button("Nộp"):
        if lesson["options"].index(ans) == lesson["correct"]:
            st.success("Đúng +10 coins")
            st.session_state.coins += 10
        else:
            st.error("Sai -5 coins")
            st.session_state.coins -= 5

# ================= ĐI LÀM =================
elif menu == "💼 Đi làm":
    task = jobs[0]["tasks"][0]

    st.subheader("Công việc hôm nay")

    st.info(boss_msg(task))

    st.write(task["description"])

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

# ================= DICTIONARY =================
elif menu == "📚 Từ điển":
    key = st.text_input("Nhập TK")

    if key in dictionary:
        st.success(dictionary[key])
        
elif menu == "🎓 Lớp học AI":

    st.header("🎓 Lớp học AI (Real-time)")

    # ===== INIT STATE =====
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "coins" not in st.session_state:
        st.session_state.coins = 100

    # ===== HIỂN THỊ CHAT =====
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"🧑‍🎓 **Bạn:** {msg['content']}")
        else:
            st.markdown(f"👨‍🏫 **Giáo viên:** {msg['content']}")

    st.divider()

    # ===== INPUT =====
    user_input = st.text_input("Nhập câu trả lời hoặc câu hỏi")

    if st.button("Gửi"):
        if user_input.strip() != "":

            # lưu câu hỏi
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })

            # gọi AI
            reply = classroom_chat(
                st.session_state.chat_history,
                user_input
            )

            # lưu phản hồi
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
        st.session_state.chat_history = []
        st.rerun()
