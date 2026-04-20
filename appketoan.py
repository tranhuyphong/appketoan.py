import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
# Import đúng tên biến từ data.py
from data import ACADEMY_DATA 

# --- 1. KHỞI TẠO CẤU HÌNH ---
st.set_page_config(page_title="Học Viện Kế Toán Slay", layout="wide", page_icon="💅")

# --- 2. KHỞI TẠO SESSION STATE (CHỐNG LỖI NAMEERROR/KEYERROR) ---
if "current_phase" not in st.session_state:
    st.session_state.current_phase = "PHASE_1"
if "current_mod" not in st.session_state:
    st.session_state.current_mod = "M1"
if "lesson_idx" not in st.session_state:
    st.session_state.lesson_idx = 0
if "coins" not in st.session_state:
    st.session_state.coins = 100

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("💅 Kế Toán Slay")
    st.metric("Ví Tiền", f"{st.session_state.coins} Xu")
    
    # Chọn Phase
    phase_list = list(ACADEMY_DATA.keys())
    sel_phase = st.selectbox("Chọn Chặng:", phase_list, 
                             format_func=lambda x: ACADEMY_DATA[x]["name"])
    
    # Nếu đổi Phase thì reset Module và Lesson để tránh KeyError
    if sel_phase != st.session_state.current_phase:
        st.session_state.current_phase = sel_phase
        st.session_state.current_mod = list(ACADEMY_DATA[sel_phase]["modules"].keys())[0]
        st.session_state.lesson_idx = 0
        st.rerun()

    # Chọn Module
    modules = ACADEMY_DATA[st.session_state.current_phase]["modules"]
    sel_mod = st.radio("Học phần:", list(modules.keys()), 
                       format_func=lambda x: f"{'🔒' if modules[x]['is_premium'] else '📖'} {modules[x]['name']}")
    
    if sel_mod != st.session_state.current_mod:
        st.session_state.current_mod = sel_mod
        st.session_state.lesson_idx = 0
        st.rerun()

    if st.button("🔄 Học lại từ đầu"):
        st.session_state.current_phase = "PHASE_1"
        st.session_state.current_mod = "M1"
        st.session_state.lesson_idx = 0
        st.rerun()

# --- 4. HIỂN THỊ NỘI DUNG ---
module = ACADEMY_DATA[st.session_state.current_phase]["modules"][st.session_state.current_mod]

if module["is_premium"] and st.session_state.coins < 500:
    st.error("✨ Đây là nội dung Premium!")
    st.info("Bạn cần tích lũy đủ 500 Xu từ Chặng 1 để mở khóa. Cố lên nhé!")
else:
    lessons = module["lessons"]
    if not lessons:
        st.info("🚧 Module này đang được biên soạn nội dung...")
    else:
        lesson = lessons[st.session_state.lesson_idx]
        
        st.caption(f"{ACADEMY_DATA[st.session_state.current_phase]['name']} > {module['name']}")
        st.title(f"Bài {st.session_state.lesson_idx + 1}: {lesson['title']}")
        
        tab_theory, tab_case, tab_quiz = st.tabs(["📚 Lý Thuyết", "🧠 Case Study", "✍️ Bài Tập"])
        
        with tab_theory:
            st.markdown(lesson["theory"])
            
        with tab_case:
            st.info(f"📍 **Tình huống:** {lesson['case_study']}")
            
        with tab_quiz:
            for i, ex in enumerate(lesson["exercises"]):
                st.write(f"**Câu {i+1}:** {ex['q']}")
                ans = st.radio("Chọn đáp án:", ex['options'], key=f"q_{lesson['id']}_{i}")
                if st.button("Kiểm tra", key=f"btn_{lesson['id']}_{i}"):
                    if ans == ex['correct']:
                        st.success("Slay quá! +20 Xu")
                        st.session_state.coins += 20
                        st.balloons()
                    else:
                        st.error("Chưa đúng rồi sếp ơi!")

        # Điều hướng bài học
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.lesson_idx > 0:
                if st.button("⬅️ Bài trước"):
                    st.session_state.lesson_idx -= 1
                    st.rerun()
        with col2:
            if st.session_state.lesson_idx < len(lessons) - 1:
                if st.button("Bài tiếp theo ➡️"):
                    st.session_state.lesson_idx += 1
                    st.rerun()
