// Nếu service quá lớn, chia nhỏ làm từng phần và test từng service

[OBJECTIVE]
Đây là service <Tên service>, chịu trách nhiệm duy nhất cho <chức năng>.
Mục tiêu: <kết quả cụ thể mà service phải trả về>

[INPUT SPECIFICATION]
- Input type:
- Input description:
- Assumptions:

[CONTEXT]
<Chỉ thông tin cần thiết cho service này>
<Không lặp system prompt>

Cấu trúc dự án:

services/kg_pipeline/
├── config/ (đã có load và logging config)
│   └── .yaml          # default logic queries
├── src/ (chỉ chứa xử lí logic)
│   ├
│   ├
│   └
├── ...
├── scripts/ (chạy chương trình chính, cấu hình môi trường, dạng sh)
├── main.py (entry point logic, dùng chung cho nhiều môi trường)
├── log-service/ (đã có)
├── tests/ (test các chức năng cơ bản trong service, các xây dựng test local)
├── Dockerfile
└── requirements.txt
└── .env.example (cấu hình các biến môi trường ví dụ để sử dụng test local, ví dụ sau này triển khai lên K8S)
└── readme.md (mô tả cơ bản về service, cấu trúc thư mục, cách chạy local, ci/cd)

config yaml chỉ cấu hình logic, env sẽ cấu hình khi thay đổi môi trường

[YÊU CẦU]

<Ví dụ: Làm manual: 3 phần cần code cho dễ scalability: tài liệu thêm vào, schema, parser.py>

[CONSTRAINTS]
- Phạm vi xử lý:
- Không làm:
- Giới hạn (thời gian, độ dài, tài nguyên):
- Nên test ở local trước khi triển khai lên K8S

[ASSUMPTION]

Ví dụ: <Đưa ra template file markdown để tôi tự điền manual, dễ dàng scale sau này>

[PROCESS GUIDELINE]
- Bước 1:
- Bước 2:
- Bước 3:

[OUTPUT SPECIFICATION]
- Output format:
+ <Trả lời giả định>: <Format: 1 dòng, 2 dòng, gồm những mục nào...>
+ <Giải pháp đề xuất>: <Format: đánh giá từ 0 - 100, giải thích ưu, nhược điểm từng loại (1 dòng), giải pháp tốt nhất phân tích kĩ hơn (2 dòng)>
+ <Đưa ra kiến trúc tri tiết thư mục src, không code>
+ <Không cần kết luận, hay những câu hỏi mở thừa>

[ERROR HANDLING]
- Nếu thiếu input:
- Nếu không chắc chắn:
- Nếu xung đột dữ liệu:

[QUALITY CHECK]
- Tiêu chí đúng:
- Tiêu chí sai: