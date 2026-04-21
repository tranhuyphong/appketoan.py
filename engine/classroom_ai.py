import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def classroom_chat(history, user_input):

    messages = [
        {
            "role": "system",
            "content": """
Bạn là giáo viên kế toán.

Cách dạy:
- Hỏi học sinh từng bước
- KHÔNG đưa đáp án ngay
- Nếu sai: gợi ý
- Nếu đúng: khen + nâng level
- Dạy như lớp học thật
"""
        }
    ]

    messages += history
    messages.append({"role": "user", "content": user_input})

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    reply = res.choices[0].message.content

    return reply
