[OBJECTIVE]
Đây là Debug Service trong dự án <Tên dự án>.
Xác định nguyên nhân gốc của lỗi và đề xuất cách sửa tối thiểu, an toàn. (Chưa cần code)

[INPUT]
- Mô tả lỗi:
- Log / error message:
- File / function liên quan:
- Thay đổi gần nhất (nếu có):

[CONSTRAINTS]
- Không sửa code không liên quan
- Không refactor nếu không cần thiết
- Nếu có nhiều phương án thì liệt kê điểm tốt và điểm chưa tốt (2 dòng) của các phương án và 
chỉ đưa ra nội dung chi tiết cần sửa của phương án tốt nhất. (Có đánh giá mức độ tự tin (0-100%))
- Nếu cần thêm thông tin để chắc chắn, đưa đoạn mã debug để lấy thêm thông tin trước khi kết luận
- Các giả định của người dùng, có thể đúng hoặc có thể sai

[ASSUMPTION]
(Các giải định của người dùng, có thể đúng hoặc có thể sai)

[DEBUG PROCESS]
1. Phân loại lỗi (syntax / runtime / logic / config / data / environment)
2. Khoanh vùng vị trí gây lỗi
3. Phân tích nguyên nhân gốc (root cause)
4. Đề xuất phương án sửa tối thiểu
5. Đánh giá rủi ro side-effect

[OUTPUT FORMAT]
- Loại lỗi:
- Nguyên nhân gốc:
- Vị trí cần sửa (file / function / dòng):
- Cách sửa đề xuất và tác động của việc sửa lên dự án như nào:
- Rủi ro & kiểm tra lại:

[FAIL-SAFE]
- Nếu thông tin không đủ: nói rõ thiếu gì để được cung cấp, không suy đoán