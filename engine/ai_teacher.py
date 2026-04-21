import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def teacher_explain(question, user_answer):

    prompt = f"""
Bạn là gia sư kế toán.

Câu hỏi: {question}
Học sinh chọn: {user_answer}

Hãy:
- KHÔNG đưa đáp án ngay
- Gợi ý từng bước
- Giải thích dễ hiểu
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return res.choices[0].message.content
