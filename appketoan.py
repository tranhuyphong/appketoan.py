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
    "💼 Đi làm",
    "🤖 Chấm bút toán",
    "📚 Từ điển",
    "🎓 Lớp học AI"
]) # Đảm bảo có đủ dấu đóng ngoặc tròn ) ở đây
# ================= HỌC =================
elif menu == "🎓 Lớp học AI":

    st.header("🎓 Lớp học chuẩn giáo dục")

    # ===== INIT =====
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0

    if "coins" not in st.session_state:
        st.session_state.coins = 100

    q = question_bank[st.session_state.q_index]

    # ===== HIỂN THỊ =====
    st.subheader(f"Câu hỏi {q['id']}")
    st.write(q["question"])

    answer = st.radio("Chọn đáp án:", q["options"])

    # ===== NỘP =====
    if st.button("Nộp bài"):

        correct = q["options"].index(answer) == q["correct"]

        # 📊 TRACK SKILL
        update_progress(q["skill"], correct, st.session_state)

        if correct:
            st.success("✅ Đúng +10 coins")
            st.session_state.coins += 10

            st.info(q["explain"])

            if st.button("Câu tiếp theo"):
                st.session_state.q_index += 1
                st.rerun()

        else:
            st.error("❌ Sai -5 coins")
            st.session_state.coins -= 5

            # 🤖 AI DẠY LẠI
            hint = teacher_explain(q["question"], answer)
            st.warning("🤖 Gợi ý:")
            st.write(hint)
# ================= DICTIONARY =================
elif menu == "📚 Từ điển":
    st.header("📚 Từ điển kế toán") # Thêm header cho rõ ràng
    key = st.text_input("Nhập mã tài khoản (TK)")

    if key in dictionary:
        st.success(dictionary[key])
    elif key != "":
        st.warning("Không tìm thấy tài khoản này trong từ điển.")

# ================= LỚP HỌC AI (ĐÃ TÁCH RIÊNG) =================
elif menu == "🎓 Lớp học AI":
    st.header("🎓 Lớp học AI (Real-time)")

    # ===== INIT STATE =====
    if "chat_history" not in st.session_state:
     st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "Hôm nay học phương trình kế toán.\n\n❓ Tài sản = ?"
        }
    ]
    # ===== HIỂN THỊ CHAT =====
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"🧑‍🎓 **Bạn:** {msg['content']}")
        else:
            st.markdown(f"👨‍🏫 **Giáo viên:** {msg['content']}")

    st.divider()

    # ===== INPUT =====
    # Dùng form để tránh việc bấm nút bị load lại trang quá nhiều lần
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Nhập câu trả lời hoặc câu hỏi")
        submit_button = st.form_submit_button("Gửi")

    if submit_button and user_input.strip() != "":
        # Lưu câu hỏi
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        # Gọi AI (classroom_chat)
        reply = classroom_chat(
            st.session_state.chat_history,
            user_input
        )

        # Lưu phản hồi
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
