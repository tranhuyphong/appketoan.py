# ==========================================
# MASTER DATABASE: ACCOUNTING ACADEMY FULL
# ==========================================

ACADEMY_DATA = {
    "PHASE_1": {
        "name": "📍 CHẶNG 1: KIẾN THỨC CỐT LÕI (CORE)",
        "modules": {
            "M1": {
                "name": "Module 1: Nguyên lý Kế toán (Luật chơi)",
                "is_premium": False,
                "lessons": [
                    {
                        "id": "L1.1",
                        "title": "Ngôn ngữ kinh doanh & Đối tượng kế toán",
                        "theory": "Kế toán là ngôn ngữ của kinh doanh. Đối tượng gồm: Tài sản (Assets) và Nguồn vốn (Equity & Liabilities). Phải phân biệt rõ cái gì mình sở hữu và cái gì mình đang nợ.",
                        "case_study": "Bạn mở tiệm trà sữa, bỏ ra 100tr tiền túi và vay mẹ 50tr. Tổng tài sản là 150tr. Trong đó Vốn CSH là 100tr, Nợ là 50tr.",
                        "exercises": [{"q": "Tiền gửi ngân hàng thuộc nhóm nào?", "options": ["Tài sản", "Nguồn vốn"], "correct": "Tài sản"}]
                    },
                    {"id": "L1.2", "title": "Phương trình kế toán & Ghi sổ kép", "theory": "Tổng Tài sản luôn bằng Tổng Nguồn vốn. Mọi nghiệp vụ ghi Nợ tài khoản này phải ghi Có tài khoản kia.", "case_study": "Mua máy tính 20tr trả bằng tiền mặt. Nợ 211 / Có 111. Phương trình vẫn cân.", "exercises": [{"q": "Ghi Nợ 111/Có 112 nghĩa là gì?", "options": ["Rút tiền bank về nhập quỹ", "Nộp tiền mặt vào bank"], "correct": "Rút tiền bank về nhập quỹ"}]},
                    {"id": "L1.3", "title": "Hệ thống tài khoản Thông tư 200", "theory": "Gồm 9 loại tài khoản. Đầu 1,2: Tài sản; Đầu 3,4: Nguồn vốn; Đầu 5,7: Thu nhập; Đầu 6,8: Chi phí; Đầu 9: Kết chuyển.", "case_study": "Muốn tìm tiền mặt? Nhìn vào 111. Muốn xem nợ khách hàng? Nhìn vào 131.", "exercises": [{"q": "Tài khoản đầu mấy không có số dư cuối kỳ?", "options": ["Đầu 1, 2", "Đầu 5, 6, 7, 8, 9"], "correct": "Đầu 5, 6, 7, 8, 9"}]},
                    {"id": "L1.4", "title": "Quy trình lập Báo cáo tài chính", "theory": "Từ chứng từ -> Sổ chi tiết -> Sổ cái -> Bảng cân đối tài khoản -> Báo cáo tài chính.", "case_study": "Cuối năm, kế toán phải 'chốt sổ' để sếp biết lãi hay lỗ để còn chia thưởng.", "exercises": [{"q": "Bảng nào cho biết tài sản tại một thời điểm?", "options": ["Bảng Cân đối kế toán", "Báo cáo Kết quả kinh doanh"], "correct": "Bảng Cân đối kế toán"}]}
                ]
            },
            "M2": {
                "name": "Module 2: Kế toán Tài chính thực chiến",
                "is_premium": False,
                "lessons": [
                    {"id": "L2.1", "title": "Kế toán Tiền, Phải thu & Hàng tồn kho", "theory": "Sử dụng các phương pháp tính giá xuất kho: FIFO, Bình quân gia quyền.", "case_study": "Nhập hàng giá 10, sau đó nhập giá 12. Xuất bán thì tính giá nào? Đó là nghệ thuật kế toán.", "exercises": [{"q": "Phương pháp FIFO nghĩa là gì?", "options": ["Nhập trước xuất trước", "Nhập sau xuất trước"], "correct": "Nhập trước xuất trước"}]},
                    {"id": "L2.2", "title": "Kế toán Tài sản cố định (TSCĐ)", "theory": "Điều kiện: > 30 triệu và dùng trên 1 năm. Phải trích khấu hao hàng tháng.", "case_study": "Mua xe hơi 1 tỷ dùng 10 năm. Mỗi năm chi phí khấu hao là 100tr.", "exercises": [{"q": "Tài khoản khấu hao TSCĐ là?", "options": ["211", "214"], "correct": "214"}]},
                    {"id": "L2.3", "title": "Kế toán Tiền lương & Bảo hiểm", "theory": "Tính lương (642/334) và trích bảo hiểm (338). Cập nhật tỷ lệ đóng mới nhất.", "case_study": "Nhân viên nhận 10tr net, nhưng DN phải tốn thêm ~23.5% chi phí bảo hiểm nữa.", "exercises": [{"q": "Kinh phí công đoàn do ai đóng?", "options": ["Doanh nghiệp", "Người lao động"], "correct": "Doanh nghiệp"}]},
                    {"id": "L2.4", "title": "Kế toán Tập hợp chi phí & Giá thành", "theory": "Gom 621, 622, 627 vào 154 để tính giá vốn sản phẩm.", "case_study": "Làm 1 cái bánh mất bao nhiêu tiền bột, tiền công, tiền điện? Kế toán phải tính ra được.", "exercises": [{"q": "Tài khoản thành phẩm là?", "options": ["154", "155"], "correct": "155"}]},
                    {"id": "L2.5", "title": "Kết chuyển & Xác định KQKD", "theory": "Kết chuyển doanh thu, chi phí sang 911 để tìm con số lãi/lỗ cuối cùng.", "case_study": "Doanh thu 100tr, chi phí 80tr -> Lãi 20tr. Kết chuyển Nợ 911 / Có 421.", "exercises": [{"q": "Kết chuyển chi phí ghi Nợ hay Có 911?", "options": ["Nợ 911", "Có 911"], "correct": "Nợ 911"}]}
                ]
            },
            "M3": {
                "name": "Module 3: Kế toán Quản trị",
                "is_premium": False,
                "lessons": [
                    {"id": "L3.1", "title": "Phân loại Biến phí & Định phí", "theory": "Biến phí thay đổi theo sản lượng. Định phí thì không (như tiền thuê nhà).", "case_study": "Dù bán được 1 ly hay 100 ly trà sữa, tiền thuê mặt bằng vẫn là 10tr.", "exercises": [{"q": "Tiền điện sản xuất thường là?", "options": ["Biến phí", "Định phí"], "correct": "Biến phí"}]},
                    {"id": "L3.2", "title": "Phân tích Điểm hòa vốn (CVP)", "theory": "Điểm mà Doanh thu = Chi phí. Biết điểm này để không bị lỗ.", "case_study": "Bạn cần bán bao nhiêu sản phẩm để bắt đầu có lãi?", "exercises": [{"q": "Lợi nhuận tại điểm hòa vốn bằng?", "options": ["0", "> 0"], "correct": "0"}]},
                    {"id": "L3.3", "title": "Ra quyết định ngắn hạn", "theory": "Nên tự sản xuất linh kiện hay mua ngoài cho rẻ? Kế toán quản trị sẽ trả lời.", "case_study": "Máy cũ sửa tốn 5tr, máy mới mua 10tr nhưng tiết kiệm điện. Chọn cái nào?", "exercises": [{"q": "Chi phí chìm (Sunk cost) có tính vào quyết định không?", "options": ["Có", "Không"], "correct": "Không"}]}
                ]
            },
            "M4": {
                "name": "Module 4: Thuế & Kiểm soát nội bộ",
                "is_premium": False,
                "lessons": [
                    {"id": "L4.1", "title": "Kế toán Thuế GTGT", "theory": "Phương pháp khấu trừ (133, 3331). Hóa đơn trên 20tr phải chuyển khoản.", "case_study": "Mua hàng 21tr trả tiền mặt là bị Thuế 'gõ đầu' ngay.", "exercises": [{"q": "Thuế GTGT đầu ra dùng tài khoản?", "options": ["133", "3331"], "correct": "3331"}]},
                    {"id": "L4.2", "title": "Thuế TNDN & TNCN", "theory": "Tính thuế trên lợi nhuận và thu nhập của cá nhân. Các khoản chi phí không được trừ.", "case_study": "Chi phí tiếp khách không có hóa đơn sẽ bị loại khi quyết toán thuế.", "exercises": [{"q": "Thuế suất thuế TNDN phổ thông hiện nay là?", "options": ["20%", "25%"], "correct": "20%"}]},
                    {"id": "L4.3", "title": "Kiểm soát nội bộ & Chống gian lận", "theory": "Quy trình phê duyệt chứng từ, tách biệt trách nhiệm (người giữ tiền không giữ sổ).", "case_study": "Thủ quỹ kiêm kế toán thanh toán là cơ hội vàng để 'thụt két'.", "exercises": [{"q": "Nguyên tắc bất kiêm nhiệm giúp ích gì?", "options": ["Giảm gian lận", "Tăng tốc độ làm việc"], "correct": "Giảm gian lận"}]}
                ]
            }
        }
    },
    "PHASE_2": {
        "name": "📍 CHẶNG 2: NÂNG CẤP (PREMIUM)",
        "modules": {
            "M5": {
                "name": "Module 5: Kế toán Tập đoàn",
                "is_premium": True,
                "lessons": [
                    {"id": "L5.1", "title": "Hợp nhất Báo cáo tài chính", "theory": "Loại trừ giao dịch nội bộ giữa công ty mẹ và con.", "case_study": "Mẹ bán cho con 1 tỷ, con chưa bán ra ngoài. Tập đoàn chưa thực lãi 1 tỷ đó.", "exercises": [{"q": "Công ty con là công ty mẹ nắm giữ bao nhiêu quyền biểu quyết?", "options": ["> 50%", "> 20%"], "correct": "> 50%"}]},
                    {"id": "L5.2", "title": "Giao dịch liên kết & Chuyển giá", "theory": "Chống việc chuyển lợi nhuận sang nơi có thuế suất thấp hơn.", "case_study": "Tại sao các tập đoàn lớn hay đặt trụ sở tại 'thiên đường thuế'?", "exercises": [{"q": "BEPS là thuật ngữ liên quan đến?", "options": ["Chống xói mòn cơ sở thuế", "Phần mềm kế toán"], "correct": "Chống xói mòn cơ sở thuế"}]}
                ]
            },
            "M6": {
                "name": "Module 6: Kế toán Pháp y (Forensic)",
                "is_premium": True,
                "lessons": [
                    {"id": "L6.1", "title": "Nhận diện xào nấu sổ sách", "theory": "Thủ thuật ghi nhận doanh thu ảo, giấu nợ.", "case_study": "Soi báo cáo của Enron hay Lehman Brothers để thấy đỉnh cao của 'ảo thuật'.", "exercises": [{"q": "Mô hình Beneish M-Score dùng để?", "options": ["Phát hiện gian lận BCTC", "Tính khấu hao"], "correct": "Phát hiện gian lận BCTC"}]}
                ]
            },
            "M7": {
                "name": "Module 7: Chuẩn mực Quốc tế IFRS",
                "is_premium": True,
                "lessons": [
                    {"id": "L7.1", "title": "IFRS vs VAS", "theory": "Sự khác biệt về giá trị hợp lý (Fair Value) và giá gốc (Historical Cost).", "case_study": "Thế giới dùng IFRS, Việt Nam đang lộ trình áp dụng. Biết IFRS lương x2.", "exercises": [{"q": "IFRS ưu tiên dùng giá trị nào?", "options": ["Giá trị hợp lý", "Giá gốc"], "correct": "Giá trị hợp lý"}]}
                ]
            }
        }
    },
    "PHASE_3": {
        "name": "📍 CHẶNG 3: KỸ NĂNG THỰC CHIẾN & TECH",
        "modules": {
            "M8": {
                "name": "Module 8: Công nghệ Kế toán",
                "is_premium": False,
                "lessons": [
                    {"id": "L8.1", "title": "Phần mềm ERP & Cloud", "theory": "Sử dụng MISA, SAP, Oracle. Dữ liệu tập trung.", "case_study": "Ngồi ở nhà vẫn duyệt được phiếu chi trên điện thoại.", "exercises": [{"q": "SaaS trong kế toán nghĩa là gì?", "options": ["Phần mềm như một dịch vụ", "Hệ thống tài khoản"], "correct": "Phần mềm như một dịch vụ"}]},
                    {"id": "L8.2", "title": "Data Analytics cho Kế toán", "theory": "Dùng PowerBI, Excel nâng cao để vẽ biểu đồ tài chính.", "case_study": "Biến con số khô khan thành biểu đồ màu sắc cho sếp dễ hiểu.", "exercises": [{"q": "Pivot Table dùng để?", "options": ["Tổng hợp dữ liệu nhanh", "Soạn thảo văn bản"], "correct": "Tổng hợp dữ liệu nhanh"}]}
                ]
            },
            "M9": {
                "name": "Module 9: Luyện nghề (Career Prep)",
                "is_premium": False,
                "lessons": [
                    {"id": "L9.1", "title": "Case Study Big4 & Phỏng vấn", "theory": "Cách trả lời phỏng vấn chuyên môn và xử lý tình huống đạo đức nghề nghiệp.", "case_study": "Bị sếp ép làm sai, bạn nói gì với HR Big4 để họ nhận bạn?", "exercises": [{"q": "Yếu tố quan trọng nhất của kế toán là?", "options": ["Trung thực", "Giỏi toán"], "correct": "Trung thực"}]}
                ]
            }
        }
    }
}
