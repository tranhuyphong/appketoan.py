job_tasks = [

# ================= INTERN =================
{
    "level": 1,
    "department": "AP",
    "type": "mcq",
    "title": "Nhập hóa đơn mua hàng",
    "question": "Mua hàng 10tr chưa VAT, VAT 10%. Bút toán đúng?",
    "options": [
        "Nợ 156:10tr, Nợ 133:1tr, Có 331:11tr",
        "Nợ 156:11tr, Có 331:11tr",
        "Nợ 156:10tr, Có 111:10tr"
    ],
    "correct": 0,
    "salary": 20,
    "penalty": -10,
    "time": 20
},

{
    "level": 1,
    "department": "AR",
    "type": "mcq",
    "title": "Ghi nhận doanh thu",
    "question": "Bán hàng thu tiền mặt 5tr, bút toán?",
    "options": [
        "Nợ 111, Có 511",
        "Nợ 131, Có 511",
        "Nợ 111, Có 131"
    ],
    "correct": 0,
    "salary": 20,
    "penalty": -10,
    "time": 20
},

# ================= STAFF =================
{
    "level": 4,
    "department": "AP",
    "type": "mcq",
    "title": "Thanh toán công nợ",
    "question": "Trả NCC 20tr bằng chuyển khoản?",
    "options": [
        "Nợ 331 / Có 112",
        "Nợ 112 / Có 331",
        "Nợ 331 / Có 111"
    ],
    "correct": 0,
    "salary": 40,
    "penalty": -20,
    "time": 25
},

{
    "level": 4,
    "department": "TAX",
    "type": "mcq",
    "title": "Thuế GTGT",
    "question": "Thuế GTGT đầu vào được khấu trừ ghi vào đâu?",
    "options": [
        "133",
        "3331",
        "511"
    ],
    "correct": 0,
    "salary": 40,
    "penalty": -20,
    "time": 25
},

# ================= SENIOR =================
{
    "level": 7,
    "department": "GL",
    "type": "case",
    "title": "Kiểm tra sai lệch sổ cái",
    "question": """
Sổ cái lệch 50 triệu.
Phát hiện do ghi thiếu chi phí.

Hỏi: xử lý thế nào?
""",
    "options": [
        "Bỏ qua",
        "Ghi bổ sung chi phí",
        "Xóa dữ liệu"
    ],
    "correct": 1,
    "salary": 80,
    "penalty": -40,
    "time": 40
},

{
    "level": 7,
    "department": "AR",
    "type": "case",
    "title": "Khách hàng không trả tiền",
    "question": """
Khách nợ 100tr quá hạn 6 tháng.

Bạn xử lý?
""",
    "options": [
        "Bỏ qua",
        "Trích lập dự phòng",
        "Xóa luôn"
    ],
    "correct": 1,
    "salary": 80,
    "penalty": -40,
    "time": 40
},

# ================= MANAGER =================
{
    "level": 10,
    "department": "TAX",
    "type": "case",
    "title": "Thanh tra thuế",
    "question": """
Cơ quan thuế kiểm tra, phát hiện thiếu doanh thu 500tr.

Bạn xử lý?
""",
    "options": [
        "Chối",
        "Điều chỉnh + nộp phạt",
        "Xóa dữ liệu"
    ],
    "correct": 1,
    "salary": 150,
    "penalty": -80,
    "time": 60
},

{
    "level": 10,
    "department": "GL",
    "type": "case",
    "title": "Báo cáo tài chính sai",
    "question": """
Lợi nhuận bị âm do ghi sai chi phí.

Bạn làm gì?
""",
    "options": [
        "Giữ nguyên",
        "Điều chỉnh lại bút toán",
        "Ẩn báo cáo"
    ],
    "correct": 1,
    "salary": 150,
    "penalty": -80,
    "time": 60
},

]
