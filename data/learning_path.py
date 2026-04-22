learning_path = [

# ================= LEVEL 1 =================
{
    "level": "🟢 Beginner",
    "unlock_coins": 0,
    "modules": [

        {
            "name": "Nguyên lý Kế toán",
            "lessons": [

                {
                    "id": "asset",
                    "title": "Tài sản là gì?",
                    "xp": 20,
                    "content": """
Tài sản là tất cả những gì doanh nghiệp sở hữu và có thể tạo ra giá trị kinh tế.

Ví dụ:
- Tiền mặt
- Hàng tồn kho
- Máy móc
- Khoản phải thu

👉 Quy tắc: Tài sản LUÔN có số dư bên Nợ
""",
                    "quiz": [
                        {
                            "question": "Tài sản là gì?",
                            "options": [
                                "Nguồn vốn của doanh nghiệp",
                                "Những gì doanh nghiệp sở hữu",
                                "Chi phí phát sinh"
                            ],
                            "answer": 1
                        },
                        {
                            "question": "Tài sản có số dư bên nào?",
                            "options": ["Nợ", "Có"],
                            "answer": 0
                        }
                    ]
                },

                {
                    "id": "liability",
                    "title": "Nguồn vốn là gì?",
                    "xp": 20,
                    "content": """
Nguồn vốn là nơi hình thành nên tài sản.

Gồm:
- Nợ phải trả
- Vốn chủ sở hữu

👉 Quy tắc: Có số dư bên Có
""",
                    "quiz": [
                        {
                            "question": "Nguồn vốn gồm gì?",
                            "options": [
                                "Tài sản",
                                "Nợ và vốn chủ",
                                "Doanh thu"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "equation",
                    "title": "Phương trình kế toán",
                    "xp": 30,
                    "content": """
Tài sản = Nợ phải trả + Vốn chủ sở hữu

👉 Mọi nghiệp vụ phải giữ cân bằng
""",
                    "quiz": [
                        {
                            "question": "Phương trình kế toán?",
                            "options": [
                                "Tài sản = Nợ + Vốn",
                                "Doanh thu = Chi phí"
                            ],
                            "answer": 0
                        }
                    ]
                }
            ]
        },

        {
            "name": "Kế toán cơ bản",
            "lessons": [

                {
                    "id": "cash",
                    "title": "Kế toán tiền",
                    "xp": 25,
                    "content": """
Tiền gồm:
- 111: Tiền mặt
- 112: Ngân hàng

👉 Tiền tăng → Nợ
""",
                    "quiz": [
                        {
                            "question": "Tiền tăng ghi gì?",
                            "options": ["Nợ", "Có"],
                            "answer": 0
                        }
                    ]
                },

                {
                    "id": "inventory",
                    "title": "Hàng tồn kho",
                    "xp": 25,
                    "content": """
Mua hàng:
- Nợ 156
- Có 111/331
""",
                    "quiz": [
                        {
                            "question": "Mua hàng ghi gì?",
                            "options": ["Nợ 156", "Có 156"],
                            "answer": 0
                        }
                    ]
                }

            ]
        }

    ]
},

# ================= LEVEL 2 =================
{
    "level": "🔵 Professional",
    "unlock_coins": 200,
    "modules": [

        {
            "name": "Kế toán chi phí",
            "lessons": [

                {
                    "id": "cost621",
                    "title": "Chi phí NVL (621)",
                    "xp": 30,
                    "content": """
Xuất kho:
- Nợ 621
- Có 152
""",
                    "quiz": [
                        {
                            "question": "Xuất NVL ghi gì?",
                            "options": ["Nợ 621", "Có 621"],
                            "answer": 0
                        }
                    ]
                }

            ]
        },

        {
            "name": "Kế toán thuế",
            "lessons": [

                {
                    "id": "vat",
                    "title": "Thuế GTGT",
                    "xp": 35,
                    "content": """
Thuế phải nộp = đầu ra - đầu vào
""",
                    "quiz": [
                        {
                            "question": "Thuế GTGT tính?",
                            "options": ["Đầu ra - đầu vào", "Ngược lại"],
                            "answer": 0
                        }
                    ]
                }

            ]
        }

    ]
},

# ================= LEVEL 3 =================
{
    "level": "🟠 Expert",
    "unlock_coins": 500,
    "modules": [

        {
            "name": "IFRS",
            "lessons": [

                {
                    "id": "ifrs",
                    "title": "IFRS là gì?",
                    "xp": 40,
                    "content": """
Chuẩn mực kế toán quốc tế
""",
                    "quiz": [
                        {
                            "question": "IFRS là gì?",
                            "options": ["VAS", "Chuẩn quốc tế"],
                            "answer": 1
                        }
                    ]
                }

            ]
        }

    ]
},

# ================= LEVEL 4 =================
{
    "level": "🔴 Strategist",
    "unlock_coins": 1000,
    "modules": [

        {
            "name": "AI & Future",
            "lessons": [

                {
                    "id": "ai",
                    "title": "AI trong kế toán",
                    "xp": 50,
                    "content": """
AI giúp:
- Tự động hóa
- Phân tích dữ liệu
""",
                    "quiz": [
                        {
                            "question": "AI giúp gì?",
                            "options": ["Không gì", "Tự động hóa"],
                            "answer": 1
                        }
                    ]
                }

            ]
        }

    ]
}

]
