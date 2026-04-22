import streamlit as st
import random
import datetime
import pandas as pd
import streamlit.components.v1 as components
from supabase import create_client

# ================= 1. CẤU HÌNH TRANG (PHẢI Ở ĐẦU) =================
st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ================= 2. IMPORT DỮ LIỆU & ENGINE =================
# Chú ý: Đảm bảo các file này tồn tại trong cùng thư mục project
try:
    from data.career_tasks import career_tasks
    from data.curriculum import curriculum
    from data.question_bank import question_bank
    from data.dictionary import dictionary
    from data.case_study import case_studies
    from engine.ai_teacher import teacher_explain
    from engine.progress_tracker import update_progress
    from engine.classroom_ai import classroom_chat
    from engine.boss_ai import boss_msg
    from engine.ai_grader import grade
    from engine.financial_report import generate_report
    from engine.fraud_detection import detect_fraud
    from data.finance_data import transactions
except ImportError as e:
    st.error(f"⚠️ Thiếu file hệ thống: {e}")
    # Tạo các biến trống để app không sập hoàn toàn nếu thiếu file
    curriculum = curriculum if 'curriculum' in locals() else []
    question_bank = question_bank if 'question_bank' in locals() else []

# ================= 3. KẾT NỐI SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indqd3Rvd21kY2RrcHJ5eGNxcXR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3NjY1NDMsImV4cCI6MjA5MjM0MjU0M30.jX4wAiXNezvmnwvr1hucjRxANZ5jWgzwn_9BsVCoueg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= 4. HÀM HỖ TRỢ (HELPER FUNCTIONS) =================
def render_unit_map(module_name, lessons):
    html = f"""
    <style>
    .unit {{ background: #0f172a; padding: 20px; border-radius: 20px; margin-bottom: 30px; }}
    .unit-title {{ font-size: 20px; font-weight: bold; margin-bottom: 15px; color: #f8fafc; }}
    .lesson-row {{ display: flex; gap: 15px; flex-wrap: wrap; }}
    .node {{ width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; 
               justify-content: center; font-weight: bold; color: white; cursor: pointer; transition: 0.2s; }}
    .node:hover {{ transform: scale(1.1); }}
    .done {{ background: #22c55e; }}
    .current {{ background: #3b82f6; }}
    .locked {{ background: #475569; opacity: 0.4; }}
    </style>
    <div class="unit">
        <div class="unit-title">{module_name}</div>
        <div class="lesson-row">
    """
    for i, lesson in enumerate(lessons):
        cls = "node done" if lesson["status"] == "done" else "node current" if lesson["status"] == "current" else "node locked"
        html += f"<div class='{cls}'>{i+1}</div>"
    html += "</div></div>"
    components.html(html, height=200)

def load_progress():
    try:
        res = supabase.table("users_progress").select("*").eq("email", st.session_state.user).execute()
        return {r["lesson_id"]: r for r in res.data}
    except: return {}

def save_progress(lesson_id, score):
    try:
        supabase.table("users_progress").upsert({
            "email": st.session_state.user,
            "lesson_id": lesson_id,
            "status": "done",
            "score": score,
            "last_learned": str(datetime.date.today())
        }).execute()
    except Exception as e: print("Lỗi lưu tiến trình:", e)

def save_coins():
    if "user" in st.session_state and st.session_state.user:
        try:
            supabase.table("users").upsert({
                "email": st.session_state.user,
                "coins": st.session_state.coins
            }).execute()
        except Exception as e: print(f"Lưu coin thất bại: {e}")

# ================= 5. KHỞI TẠO SESSION STATE =================
if "coins" not in st.session_state:
    st.session_state.update({
        "coins": 100, "streak": 0, "last_login": "", "percent": None,
        "lesson_progress": {}, "current_lesson": None, "q_index": 0,
        "chat_history": [], "skills": {}, "learned_lessons": [], "daily_learn": 0
    })

# ================= 6. ĐĂNG NHẬP / ĐĂNG KÝ =================
if "user" not in st.session_state:
    st.title("🚀 PHONG AI ACCOUNTING")
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
    with tab1:
        email = st.text_input("Email")
        pw = st.text_input("Password", type="password")
        if st.button("Đăng nhập"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": pw})
                if res.user:
                    st.session_state.user = res.user.email
                    st.rerun()
            except: st.error("Sai tài khoản hoặc mật khẩu!")
    with tab2:
        reg_email = st.text_input("Email đăng ký")
        reg_pw = st.text_input("Password đăng ký", type="password")
        if st.button("Thực hiện Đăng ký"):
            try:
                supabase.auth.sign_up({"email": reg_email, "password": reg_pw})
                st.success("Đăng ký xong! Hãy qua tab Đăng nhập.")
            except Exception as e: st.error(f"Lỗi: {e}")
    st.stop()

# ================= 7. TẢI DỮ LIỆU TIẾN TRÌNH =================
if "progress_loaded" not in st.session_state:
    db_progress = load_progress()
    for l_id, data in db_progress.items():
        st.session_state.lesson_progress[l_id] = {"answers": {}, "submitted": True, "score": data.get("score", 0)}
    st.session_state.progress_loaded = True

# Thưởng đăng nhập hàng ngày
today = str(datetime.date.today())
if st.session_state.last_login != today:
    st.session_state.coins += 20
    st.session_state.last_login = today
    st.toast("🎁 Daily +20 coins", icon="💰")
    save_coins()

# ================= 8. GIAO DIỆN CHÍNH =================
coins = st.session_state.coins
rank = "🥉 Intern" if coins < 100 else "🥈 Junior" if coins < 300 else "🥇 Senior" if coins < 600 else "👑 Manager"

st.sidebar.markdown(f"### 🎖️ Rank: {rank}")
st.sidebar.markdown(f"### 💰 Coins: {coins}")

menu = st.sidebar.radio("Menu", [
    "📘 Học", "🎓 Lớp học AI (Quiz)", "🎓 Lớp học AI (Chat)", "💼 Đi làm",
    "🧾 Case Study", "📊 Dashboard", "📊 Financial Report", "🤖 Chấm bút toán",
    "📚 Từ điển", "🚨 Fraud Detection", "🏆 Leaderboard"
])

# ================= 9. LOGIC CÁC MENU =================

if menu == "📘 Học":
    st.header("🗺️ Learning Map")
    for level in curriculum:
        # --- FIX LỖI KEYERROR Ở ĐÂY ---
        # Sử dụng .get() để lấy tên level, nếu không có thì lấy key 'name', nếu không có nữa thì ghi 'N/A'
        level_name = level.get('level', level.get('name', 'Level không tên'))
        
        required = level.get("unlock_coins", 0)
        unlocked = st.session_state.coins >= required

        if not unlocked:
            st.markdown(f"## 🔒 {level_name} (Cần {required} 💰)")
            st.warning("Bạn chưa đủ coin để mở khóa cấp độ này.")
            continue
        
        st.markdown(f"## 🔓 {level_name}")
        for module in level.get("modules", []):
            st.markdown(f"### 📚 {module['name']}")
            lesson_nodes = []
            prev_passed = True

            # Kiểm tra trạng thái từng bài để vẽ Map
            for lesson in module["lessons"]:
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"
                if l_id not in st.session_state.lesson_progress:
                    st.session_state.lesson_progress[l_id] = {"answers": {}, "submitted": False, "score": 0}
                
                prog = st.session_state.lesson_progress[l_id]
                status = "done" if prog["submitted"] and prog["score"] >= 70 else "current" if prev_passed else "locked"
                lesson_nodes.append({"status": status})
                prev_passed = (status == "done")

            render_unit_map(module["name"], lesson_nodes)

            # Nội dung bài học (Expander)
            prev_passed = True
            for lesson in module["lessons"]:
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"
                prog = st.session_state.lesson_progress[l_id]
                can_open = prev_passed
                
                icon = "✅" if prog["submitted"] and prog["score"] >= 70 else "⬜" if can_open else "🔒"
                
                with st.expander(f"{icon} {lesson['title']}"):
                    if not can_open:
                        st.info("Hãy hoàn thành bài học phía trước.")
                        continue
                    
                    st.write(lesson["content"])
                    st.divider()
                    
                    correct_count = 0
                    for i, q in enumerate(lesson.get("quiz", [])):
                        ans = st.radio(q["question"], q["options"], key=f"rad_{l_id}_{i}", disabled=prog["submitted"])
                        if ans == q["options"][q["answer"]]:
                            correct_count += 1
                    
                    if not prog["submitted"]:
                        if st.button("🚀 Nộp bài", key=f"btn_{l_id}"):
                            score = int((correct_count / len(lesson["quiz"])) * 100)
                            prog["submitted"] = True
                            prog["score"] = score
                            if score >= 70:
                                st.success(f"Pass! +{lesson.get('xp', 20)} coins")
                                st.session_state.coins += lesson.get('xp', 20)
                                st.session_state.daily_learn += 1
                                save_progress(l_id, score)
                            else: st.error(f"Không đạt ({score}%). Thử lại sau nhé!")
                            save_coins()
                            st.rerun()
                    else:
                        st.info(f"Kết quả bài làm: {prog['score']}%")
                prev_passed = (prog["submitted"] and prog["score"] >= 70)

elif menu == "🎓 Lớp học AI (Quiz)":
    if len(question_bank) > 0:
        q = question_bank[st.session_state.q_index % len(question_bank)]
        st.subheader(q["question"])
        ans = st.radio("Chọn đáp án:", q["options"])
        if st.button("Nộp"):
            if q["options"].index(ans) == q["correct"]:
                st.session_state.streak += 1
                reward = min(10 + st.session_state.streak * 2, 30)
                st.success(f"Chính xác! +{reward} coins")
                st.session_state.coins += reward
            else:
                st.session_state.streak = 0
                st.error("Sai rồi! -5 coins")
                st.session_state.coins -= 5
            st.info(q["explain"])
            save_coins()
        if st.button("➡️ Câu tiếp"):
            st.session_state.q_index += 1
            st.rerun()

elif menu == "🎓 Lớp học AI (Chat)":
    st.header("💬 Chat với Giảng viên AI")
    if not st.session_state.chat_history:
        st.session_state.chat_history = [{"role": "assistant", "content": "Chào bạn, hãy trả lời: Phương trình kế toán cơ bản là gì?"}]
    
    for m in st.session_state.chat_history:
        st.chat_message(m["role"]).write(m["content"])
    
    u_input = st.chat_input("Nhập câu trả lời...")
    if u_input:
        st.session_state.chat_history.append({"role": "user", "content": u_input})
        reply = classroom_chat(st.session_state.chat_history, u_input)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        if "đúng" in reply.lower(): st.session_state.coins += 10
        save_coins()
        st.rerun()

elif menu == "💼 Đi làm":
    st.header("🏢 Career Mode - Đi làm thực tế")
    if "work_day" not in st.session_state: 
        st.session_state.update({"work_day": 1, "performance": 100, "fail": 0, "stress": 0})
    
    st.info(f"📅 Ngày {st.session_state.work_day} | 📊 Hiệu suất: {st.session_state.performance}%")
    
    role_key = rank.split(" ")[1] if " " in rank else rank
    tasks = career_tasks.get(role_key, career_tasks.get("Intern", []))
    if tasks:
        task = random.choice(tasks)
        st.subheader("Nhiệm vụ hôm nay:")
        st.write(task["desc"])
        opts = [task["correct"]] + task["wrong"]
        random.shuffle(opts)
        choice = st.radio("Hướng xử lý:", opts)
        
        if st.button("🚀 Giải quyết"):
            if choice == task["correct"]:
                st.success("Sếp khen! +30 coins")
                st.session_state.coins += 30
                st.session_state.performance += 5
            else:
                st.error("Bị nhắc nhở! -20 coins")
                st.session_state.coins -= 20
                st.session_state.performance -= 10
            st.session_state.work_day += 1
            save_coins()

elif menu == "📊 Dashboard":
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Tổng Coins", st.session_state.coins)
    col2.metric("🔥 Chuỗi học (Streak)", st.session_state.streak)
    col3.metric("🎖️ Cấp bậc", rank)
    
elif menu == "🏆 Leaderboard":
    st.header("🏆 Bảng Xếp Hạng")
    try:
        res = supabase.table("users").select("email, coins").order("coins", desc=True).limit(10).execute()
        df = pd.DataFrame(res.data)
        st.table(df)
    except: st.error("Không thể tải bảng xếp hạng.")

# Thêm Footer
st.sidebar.divider()
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()
