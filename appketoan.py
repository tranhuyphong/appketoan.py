# --- TRONG FILE APP_KETOAN.PY ---
# Tìm đến phần hiển thị Lesson và thay bằng:

current_mod = ACADEMY_DATA[st.session_state.current_phase]["modules"][st.session_state.current_mod]
lessons = current_mod["lessons"]

if not lessons:
    st.warning("🚧 Bài học cho phần này đang được cập nhật. Quay lại sau nhé!")
else:
    # Đảm bảo lesson_idx không bị vượt quá khi đổi Module
    if st.session_state.lesson_idx >= len(lessons):
        st.session_state.lesson_idx = 0
        
    lesson = lessons[st.session_state.lesson_idx]
    st.caption(f"{st.session_state.current_phase} > {current_mod['name']}")
    st.title(f"Bài {st.session_state.lesson_idx + 1}: {lesson['title']}")
    
    # Progress Bar
    progress = (st.session_state.lesson_index + 1) / len(lessons) if 'lesson_index' in st.session_state else 0.5
    st.progress(progress)

    tab_learn, tab_case, tab_quiz = st.tabs(["📚 Kiến Thức", "🧠 Case Study", "✍️ Bài Tập"])
    
    with tab_learn:
        st.markdown(f"### 💡 Nội dung cốt lõi\n{lesson['theory']}")
    
    with tab_case:
        st.success(f"**Tình huống thực tế:**\n\n{lesson['case_study']}")
        
    with tab_quiz:
        for i, ex in enumerate(lesson["exercises"]):
            st.write(f"**Câu {i+1}:** {ex['q']}")
            ans = st.radio("Chọn đáp án:", ex['options'], key=f"quiz_{lesson['id']}_{i}")
            if st.button("Nộp bài", key=f"btn_{lesson['id']}_{i}"):
                if ans == ex['correct']:
                    st.balloons()
                    st.success("Quá chuẩn! +20 Xu")
                    st.session_state.coins += 20
                else:
                    st.error("Sai rồi, đọc kỹ lại Case study nhé!")

    # Navigation
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
