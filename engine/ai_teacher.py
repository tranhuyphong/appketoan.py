import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def teacher_explain(question, user_answer):
    prompt = f"""
Bạn là giáo viên kế toán.

Câu hỏi: {question}
Học sinh trả lời: {user_answer}

Nếu sai:
- KHÔNG đưa đáp án ngay
- Gợi ý từng bước
- Giải thích dễ hiểu

Nếu gần đúng:
- Khuyến khích và sửa nhẹ
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return res.choices[0].message.content
