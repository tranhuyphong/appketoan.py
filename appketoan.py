import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="Kế Toán Slay 💅", page_icon="💅", layout="wide")

# --- THIẾT LẬP API KEY (Có thêm cảnh báo nếu quên cài đặt) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.warning("⚠️ Co-founder ơi, có vẻ API Key chưa được cài đặt. Hãy thêm GEMINI_API_KEY vào Settings > Secrets trên Streamlit Cloud nhé!")

# --- ĐỊNH HÌNH CÔ GIÁO GEN Z (SYSTEM PROMPT) ---
SYSTEM_PROMPT = """
Bạn là Cô giáo Gen Z dạy Kế toán cực kỳ 'slay', thông minh và tâm lý. 
- Xưng hô: 'Chị'/'Cô' - 'Em'. 
- Phong cách: Dùng từ lóng Gen Z (vô tri, xà lơ, keo lỳ, overthinking...) và emoji 💅✨🤌.
- Chuyên môn: Phải chuẩn xác theo Thông tư 200 và Luật thuế VN.
- Phương pháp: Không đưa đáp án ngay, hãy đặt câu hỏi gợi mở để sinh viên tự tư duy.
- Nhiệm vụ: Giải đáp kiến thức và chấm điểm bài tập thực hành chứng từ.
"""

# --- KHỞI TẠO BỘ NHỚ LƯU TRỮ ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "learning_progress" not in st.session_state:
    st.session_state.learning_progress = 0
if "current_lesson" not in st.session_state:
    st.session_state.current_lesson = 0

# --- THANH SIDEBAR (ĐIỀU HƯỚNG) ---
with st.sidebar:
    st.title("💅 Kế Toán Slay v1.0")
    st.markdown("---")
    menu = st.radio(
        "Chọn khu vực học tập:",
        ["📚 Lộ trình học bài bản", "✍️ Thực hành chứng từ", "💬 Chat với Chị Đẹp AI"]
    )
    st.markdown("---")
    st.write(f"Tiến độ của em: {st.session_state.learning_progress}%")
    st.progress(min(st.session_state.learning_progress / 100, 1.0)) # Đảm bảo tối đa 100%

# ==========================================
# --- MODULE 1: LỘ TRÌNH HỌC ---
# ==========================================
if menu == "📚 Lộ trình học bài bản":
    st.header("📍 Lộ trình chinh phục Kế toán Thực tế")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Chặng 1: Nhập môn**\n\nHiểu về Tài sản, Nguồn vốn và Hóa đơn.")
        if st.button("Vào học Chặng 1"): st.session_state.current_lesson = 1
    with col2:
        st.info("**Chặng 2: Excel Kế toán**\n\nLàm chủ VLOOKUP, SUMIFS và bảng lương.")
        if st.button("Vào học Chặng 2"): st.session_state.current_lesson = 2
    with col3:
        st.info("**Chặng 3: Lên Báo cáo**\n\nTừ chứng từ sống lên Bảng CĐPS.")
        if st.button("Vào học Chặng 3"): st.session_state.current_lesson = 3

    st.markdown("---")

    # NỘI DUNG CHẶNG 1
    if st.session_state.current_lesson == 1:
        st.subheader("📖 Chặng 1: Tài sản & Nguồn vốn - 'Flex' và 'Áp lực'")
        st.write("Chào mừng em đến với bài học đầu tiên! Kế toán thực ra chỉ xoay quanh 2 thứ này thôi nè: 🤌")
        
        col_ts, col_nv = st.columns(2)
        with col_ts:
            st.success("**💎 TÀI SẢN (Assets - Cột Flex)**")
            st.write("Là những gì công ty em ĐANG CÓ. Có thể sờ được (tiền mặt, máy móc) hoặc vô hình (tiền khách hàng nợ).")
        with col_nv:
            st.warning("**🏋️ NGUỒN VỐN (Equity & Liabilities - Cột Nguồn gốc)**")
            st.write("Là nguồn hình thành nên Tài sản. Hoặc là tiền túi (Vốn chủ sở hữu), hoặc là đi vay (Nợ phải trả - áp lực nha 🥲).")
        
        st.info("**✨ Thần chú Kế toán:** Mọi sự 'flex' đều phải có nguồn gốc. Do đó: **TÀI SẢN = NGUỒN VỐN**")
        
        st.write("---")
        st.write("**🧠 Mini Test nhanh nè:**")
        answer = st.radio(
            "Công ty mua 1 dàn máy tính 50 củ nhưng CHƯA THANH TOÁN. Vậy 'Áp lực' (Nợ phải trả) của công ty tăng hay giảm?", 
            ["Chưa chọn", "Tăng lên", "Giảm đi"]
        )
        
        if answer == "Tăng lên":
            st.balloons()
            st.success("Chuẩn luôn! 10 điểm không có nhưng! Mua chịu thì nợ phải tăng chứ sao nữa 💅")
            if st.button("Hoàn thành Chặng 1 ✨"):
                st.session_state.learning_progress = min(st.session_state.learning_progress + 30, 100)
                st.session_state.current_lesson = 0
                st.rerun() # Tải lại trang để chốt tiến độ
        elif answer == "Giảm đi":
            st.error("Khoan, dừng khoảng chừng là 2 giây! 🤌 Mua chịu chưa trả tiền thì mình phải gánh thêm nợ chứ sao nợ lại giảm được. Nghĩ lại nè 🥲")

    elif st.session_state.current_lesson == 2:
        st.subheader("📖 Chặng 2: Excel Kế toán (Đang cập nhật...)")
        st.write("Chị đang soạn tài liệu hàm VLOOKUP cho mấy đứa, đợi xíu nha! 🥲")
        
    elif st.session_state.current_lesson == 3:
        st.subheader("📖 Chặng 3: Lên Báo cáo (Đang cập nhật...)")
        st.write("Đang tải dữ liệu Bảng cân đối phát sinh... ✨")

# ==========================================
# --- MODULE 2: THỰC HÀNH CHỨNG TỪ ---
# ==========================================
elif menu == "✍️ Thực hành chứng từ":
    st.header("🧾 Thực hành bóc tách chứng từ thật")
    st.write("Nhìn hóa đơn dưới đây và hạch toán cho chị xem nào! 💅")
    
    st.image("https://invoice.misa.vn/wp-content/uploads/2021/08/mau-hoa-don-gtgt-1.jpg", width=600)
    
    with st.container(border=True):
        col_a, col_b = st.columns(2)
        with col_a:
            no_tk = st.text_input("Nợ TK (ví dụ: 156):")
            thue_tk = st.text_input("Thuế GTGT Nợ (nếu có):")
        with col_b:
            co_tk = st.text_input("Có TK (ví dụ: 331):")
            so_tien = st.number_input("Tổng giá trị thanh toán (VNĐ):", step=1000)

        if st.button("Nộp bài cho Chị Đẹp chấm ✨"):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                check_query = f"""
                Sinh viên hạch toán hóa đơn mua hàng như sau: Nợ {no_tk}, Thuế {thue_tk}, Có {co_tk}, Số tiền {so_tien}.
                Biết đáp án đúng là Nợ 156, Nợ 1331, Có 331. Số tiền 11.000.000.
                Hãy dùng giọng Gen Z chấm bài và chỉ ra lỗi sai nếu có.
                """
                with st.spinner("Chị đang soi bài... 🤌"):
                    response = model.generate_content([SYSTEM_PROMPT, check_query])
                    st.chat_message("assistant", avatar="👩‍🏫").write(response.text)
                    st.session_state.learning_progress = min(st.session_state.learning_progress + 20, 100)
            except Exception as e:
                st.error(f"Ối, lỗi chấm bài rồi: {e}. Co-founder kiểm tra lại API Key nhé!")

# ==========================================
# --- MODULE 3: CHAT VỚI AI ---
# ==========================================
elif menu == "💬 Chat với Chị Đẹp AI":
    st.header("💬 Hỏi đáp cùng Cô giáo Gen Z")
    st.caption("Mọi thắc mắc về nợ có, thuế má cứ 'ting ting' chị trả lời hết! 🤌")

    # Hiển thị lịch sử chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="👩‍🏫" if msg["role"]=="assistant" else "🧑‍🎓"):
            st.write(msg["content"])

    if prompt := st.chat_input("Chị ơi, lệch bảng cân đối thì làm sao ạ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.write(prompt)

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]])
            full_query = f"{SYSTEM_PROMPT}\n\nLịch sử:\n{history_context}\n\nCâu hỏi mới: {prompt}"
            
            with st.spinner("Chị đang 'load' kiến thức..."):
                response = model.generate_content(full_query)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant", avatar="👩‍🏫"):
                    st.write(response.text)
        except Exception as e:
            st.error(f"Hệ thống báo lỗi: {e}")
            st.info("💡 Lỗi này thường do chưa cài đặt API Key trong Settings > Secrets trên trang Streamlit Cloud đó!")
