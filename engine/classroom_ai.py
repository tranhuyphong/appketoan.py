def classroom_chat(history, user_input):

    messages = [
        {
            "role": "system",
            "content": """
Bạn là giáo viên kế toán đang dạy học sinh.

LUẬT:
1. Luôn bắt đầu bằng việc giảng ngắn (1-2 câu)
2. SAU ĐÓ PHẢI đặt 1 câu hỏi cụ thể
3. KHÔNG nói lan man
4. KHÔNG cho đáp án ngay

Khi học sinh trả lời:
- Nếu đúng: khen + hỏi tiếp
- Nếu sai: gợi ý + hỏi lại

Luôn giữ format:

📘 Giảng:
...

❓ Câu hỏi:
...
"""
        }
    ]

    messages += history
    messages.append({"role": "user", "content": user_input})

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    return res.choices[0].message.content
