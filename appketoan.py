import streamlit as st
import pandas as pd
import io
import google.generativeai as genai
from PIL import Image
from data import SYSTEM_PROMPT, LESSONS

# --- CẤU HÌNH ---
st.set_page_config(page_title="Kế Toán Slay 💅", layout="wide", page_icon="💅")

try:
    api_key = st.secrets.get("GEMINI_API_KEY") or "YOUR_API_KEY_HERE"
    genai.configure(api_key=api_key)
    model_flash = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ Cần config API Key trong mục Secrets để dùng AI!")

# --- KHỞI TẠO BỘ NHỚ ---
if "coins" not in st.session_state: st.session_state.coins = 100
if "current_lesson" not in st.session_state: st.session_state.current_lesson = 1
if "interview_log" not in st.session_state: st.session_state.interview_log = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("💅 Kế Toán Slay")
    st.markdown(f"### 💰 Ví Tiền: `{st.session_state.coins} Xu`")
    st.write("---")
    prog = st.session_state.current_lesson / len(LESSONS)
    st.write(f"Tiến độ thăng chức: {int(prog*100)}%")
    st.progress(prog)
    if st.button("🔄 Học lại từ đầu"):
        st.session_state.current_lesson = 1
        st.session_state.coins = 100
        st.rerun()

# --- NỘI DUNG CHÍNH ---
# Đã sửa lỗi lặp từ "Chặng"
st.title(f"{LESSONS[st.session_state.current_lesson]['title']}")

tabs = st.tabs(["📚 Bài Học", "🎮 Quiz Tích Điểm", "📸 AI Soi Hóa Đơn", "📊 AI Chấm Excel", "🤝 Phỏng Vấn Giả Lập"])

# TAB 1: BÀI HỌC
# TAB 1: BÀI HỌC
with tabs[0]:
    st.info(LESSONS[st.session_state.current_lesson]["theory"])
    st.markdown("---")
    st.warning("👉 **Nạp xong kiến thức rồi thì mạnh dạn bấm sang tab '🎮 Quiz Tích Điểm' ở bên cạnh để làm bài test kiếm Xu qua màn nha em ơi!** 💸")

# TAB 2: QUIZ
with tabs[1]:
    st.subheader("Bấm đúng là có tiền, bấm sai là trừ lương! 💸")
    q_data = LESSONS[st.session_state.current_lesson]["quizzes"]
    all_ok = True
    for i, q in enumerate(q_data):
        st.write(f"**Câu {i+1}:** {q['question']}")
        ans = st.radio("Chọn đáp án:", ["Chưa chọn"] + q["options"], key=f"ans_{st.session_state.current_lesson}_{i}")
        if ans == q["correct_answer"]:
            st.success(q["success_msg"])
        elif ans != "Chưa chọn":
            st.error(q["error_msg"])
            st.session_state.coins = max(0, st.session_state.coins - 5)
            all_ok = False
        else: all_ok = False

    if all_ok:
        st.balloons()
        if st.button("Lên Chặng Tiếp Theo 🚀"):
            st.session_state.coins += 50
            st.session_state.current_lesson = min(st.session_state.current_lesson + 1, len(LESSONS))
            st.rerun()

# TAB 3: AI VISION
with tabs[2]:
    st.subheader("🕵️‍♀️ Chế độ: Cán Bộ Thuế Tinh Mắt")
    file_img = st.file_uploader("Quăng tờ hóa đơn vào đây chị soi cho!", type=['jpg','png','jpeg'])
    if file_img:
        img = Image.open(file_img)
        st.image(img, width=400)
        if st.button("Soi Lỗi Ngay"):
            with st.spinner("Đang soi từng con số..."):
                prompt = "Bạn là cán bộ thuế khó tính, soi bức ảnh hóa đơn này và chỉ ra lỗi sai về MST, số tiền, ngày tháng bằng ngôn ngữ Gen Z slay."
                res = model_flash.generate_content([prompt, img])
                st.write(res.text)

# TAB 4: AI EXCEL
with tabs[3]:
    st.subheader("📊 Trợ Lý Kiểm Toán AI")
    
    st.write("👉 **Bước 1: Tải bài tập mẫu về làm trước nha**")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_inv = pd.DataFrame({
            'Ngày': ['01/12', '05/12'], 
            'Nội dung': ['Mua máy tính', 'Rút tiền mặt'], 
            'TK Nợ': ['...', '...'],
            'TK Có': ['...', '...'],
            'Số tiền': [15000000, 5000000]
        })
        df_inv.to_excel(writer, sheet_name='Bai_Tap', index=False)
    
    st.download_button(
        label="📥 Tải File Excel Bài Tập", 
        data=buffer.getvalue(), 
        file_name="Bai_Tap_Ke_Toan.xlsx", 
        mime="application/vnd.ms-excel"
    )
    
    st.markdown("---")
    st.write("👉 **Bước 2: Nộp file em đã giải vào đây để chị chấm!**")
    file_ex = st.file_uploader("Nộp file Excel (.xlsx)", type=['xlsx'])
    if file_ex:
        df = pd.read_excel(file_ex)
        st.dataframe(df.head())
        if st.button("Chấm Điểm"):
            with st.spinner("Đang soát sổ..."):
                prompt = f"Đây là dữ liệu kế toán sinh viên làm: {df.to_string()}. Hãy nhận xét đúng sai ở các cột TK Nợ / TK Có và nhắc nhở bằng giọng Gen Z."
                res = model_flash.generate_content(prompt)
                st.write(res.text)

# TAB 5: INTERVIEW
with tabs[4]:
    st.subheader("🤝 Chat với Giám Đốc Tài Chính (CFO)")
    if st.button("Bắt đầu phỏng vấn"):
        st.session_state.interview_log = [{"role":"assistant", "content":"Chào em, tại sao anh nên thuê em làm kế toán thay vì thuê AI?"}]
    
    for m in st.session_state.interview_log:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    if chat_input := st.chat_input("Trả lời sếp..."):
        st.session_state.interview_log.append({"role":"user", "content":chat_input})
        with st.chat_message("user"): st.write(chat_input)
        with st.spinner("Sếp đang gõ..."):
            res = model_flash.generate_content(f"Bạn là CFO sắc sảo. Phỏng vấn ứng viên này dựa trên hội thoại: {str(st.session_state.interview_log)}")
            st.session_state.interview_log.append({"role":"assistant", "content":res.text})
            st.rerun()
