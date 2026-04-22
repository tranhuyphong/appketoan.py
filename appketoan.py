import streamlit as st
import random
import datetime
import pandas as pd
import streamlit.components.v1 as components
from supabase import create_client

# ================= 1. CONFIG =================
st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ================= 2. IMPORT =================
try:
    from data.career_tasks import career_tasks
    from data.curriculum import curriculum
    from data.question_bank import question_bank
    from data.dictionary import dictionary
    from data.case_study import case_studies
    from engine.classroom_ai import classroom_chat
    from engine.boss_ai import boss_msg
except:
    curriculum = []
    question_bank = []

# ================= 3. SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indqd3Rvd21kY2RrcHJ5eGNxcXR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3NjY1NDMsImV4cCI6MjA5MjM0MjU0M30.jX4wAiXNezvmnwvr1hucjRxANZ5jWgzwn_9BsVCoueg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= 4. MAP UI =================
def render_duolingo_pro(unit_id, lessons):
    html = """
    <style>
    .map { display: flex; flex-direction: column; align-items: center; gap: 35px; }
    .row { width: 100%; display: flex; }
    .left { justify-content: flex-start; padding-left: 20%; }
    .right { justify-content: flex-end; padding-right: 20%; }

    .node {
        width: 75px; height: 75px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; color: white; cursor: pointer;
    }

    .done { background: #22c55e; }
    .current { background: #3b82f6; }
    .locked { background: #334155; opacity: 0.4; cursor: not-allowed; }
    .boss { background: gold; color: black; }
    .exam { background: purple; }

    .line { width: 6px; height: 40px; background: #475569; }
    </style>

    <div class="map">
    """

    for i, lesson in enumerate(lessons):
        cls = f"node {lesson['status']}"
        if lesson.get("type") == "boss":
            cls += " boss"
        elif lesson.get("type") == "exam":
            cls += " exam"

        side = "left" if i % 2 == 0 else "right"
        label = lesson.get("label", i+1)

        click = f"sendClick('{unit_id}|{i}')" if lesson["status"] != "locked" else ""

        html += f"""
        <div class="row {side}">
            <div class="{cls}" onclick="{click}">
                {label}
            </div>
        </div>
        """

        if i < len(lessons)-1:
            html += "<div class='line'></div>"

    html += "</div>"

    components.html(f"""
    {html}
    <script>
    function sendClick(val){{
        window.parent.postMessage({{
            type: "streamlit:setSessionState",
            key: "clicked_node",
            value: val
        }}, "*");
    }}
    </script>
    """, height=600)

# ================= 5. STATE =================
if "coins" not in st.session_state:
    st.session_state.update({
        "coins": 120,
        "streak": 0,
        "lesson_progress": {},
        "current_lesson": None
    })

# ================= 6. UI =================
st.sidebar.markdown(f"💰 Coins: {st.session_state.coins}")

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

# ================= 7. LEARNING MAP =================
if menu == "📘 Học":
    st.header("🗺️ Learning Map")

    # SHOW LESSON
    if st.session_state.get("current_lesson"):
        lesson = st.session_state.current_lesson
        st.subheader(lesson["title"])
        st.write(lesson["content"])

        if st.button("❌ Đóng"):
            st.session_state.current_lesson = None
            st.rerun()

    for level in curriculum:
        level_name = level.get("level", "Unknown")
        required = level.get("unlock_coins", 0)

        st.markdown(f"## {'🔓' if st.session_state.coins >= required else '🔒'} {level_name}")

        for module in level.get("modules", []):
            st.markdown(f"### 📚 {module['name']}")

            lesson_nodes = []
            prev_passed = True

            # 🔥 BUILD NODE + AUTO ADD BOSS/EXAM
            lessons_full = module["lessons"].copy()

            lessons_full.append({
                "title": "Boss Fight",
                "type": "boss"
            })

            lessons_full.append({
                "title": "Final Exam",
                "type": "exam"
            })

            for i, lesson in enumerate(lessons_full):
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"

                if l_id not in st.session_state.lesson_progress:
                    st.session_state.lesson_progress[l_id] = {"submitted": False, "score": 0}

                prog = st.session_state.lesson_progress[l_id]

                if prog["submitted"]:
                    status = "done"
                elif prev_passed:
                    status = "current"
                else:
                    status = "locked"

                lesson_nodes.append({
                    "status": status,
                    "type": lesson.get("type", "normal"),
                    "label": "👑" if lesson.get("type") == "boss" else "🎓" if lesson.get("type") == "exam" else i+1
                })

                prev_passed = (status == "done")

            render_duolingo_pro(module["name"], lesson_nodes)

            # ✅ FIX CLICK
            clicked = st.session_state.get("clicked_node")

            if clicked and "|" in clicked:
                unit, index = clicked.split("|")

                if unit == module["name"]:
                    idx = int(index)
                    selected = lessons_full[idx]

                    st.session_state.current_lesson = selected
                    st.session_state.clicked_node = None
                    st.rerun()

# ================= 8. QUIZ =================
elif menu == "🎓 Lớp học AI (Quiz)":
    if question_bank:
        q = random.choice(question_bank)
        st.subheader(q["question"])
        ans = st.radio("Chọn:", q["options"])

        if st.button("Nộp"):
            if q["options"].index(ans) == q["correct"]:
                st.success("Đúng!")
                st.session_state.coins += 10
            else:
                st.error("Sai!")

# ================= 9. CHAT =================
elif menu == "🎓 Lớp học AI (Chat)":
    st.write("Chat AI đang hoạt động...")

# ================= 10. LEADERBOARD =================
elif menu == "🏆 Leaderboard":
    st.write("Top người chơi")

# ================= LOGOUT =================
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()
