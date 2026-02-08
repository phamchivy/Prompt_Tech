[ROLE]
Bạn có nhiệm vụ đọc – tổng hợp – chuẩn hóa các đoạn hội thoại kỹ thuật rời rạc
thành một bức tranh kiến trúc toàn cục, mạch lạc và có thể dùng làm tài liệu báo cáo.

[OBJECTIVE]
Từ toàn bộ nội dung hội thoại phía dưới, hãy:
- Nắm được toàn cảnh service
- Chuẩn hóa lại thành tư duy kiến trúc
- Loại bỏ chi tiết trao đổi vụn vặt
- Giữ lại quyết định kỹ thuật, lý do và trade-off

[INPUT]
Toàn bộ nội dung chat triển khai Knowledge Graph cho NRF và NSSF (theo thứ tự thời gian).

[CONTEXT]
Service name:
Domain:
Mục đích service:
Vai trò của service trong hệ thống lớn hơn (nếu có):
Mức độ production / research / PoC:

[ANALYSIS GUIDELINES]
- Không tự suy đoán nếu thiếu thông tin quan trọng
- Nếu thiếu, liệt kê vào "Open questions"
- Ưu tiên tư duy kiến trúc, không sa vào code chi tiết
- Nêu rõ các quyết định đã được chốt vs còn thử nghiệm
- Nếu có nhiều hướng được bàn, hãy so sánh ngắn gọn

[ANALYSIS STEPS]
1. Input – Output của service
2. Các module chính được thảo luận
3. Các quyết định kiến trúc quan trọng (và lý do)
4. Những giới hạn / rủi ro đã được nhắc tới
5. Những điểm còn bỏ ngỏ

[OUTPUT FORMAT]

=== Service Summary ===
Problem formulation:
Service scope & responsibility:
System role:

=== Architecture ===
High-level architecture:
Main components:
Data flow (textual):

=== Technical Decisions ===
Decision 1:
- Choice:
- Reason:
- Trade-off:

Decision 2:
...

=== Technology Stack ===
Schemas, Relations, Entities,...


=== Risks & Limitations ===
- ...

=== Open Questions / TODO ===
- ...

=== Report-ready Abstract (5–7 dòng) ===
(Viết lại service này theo văn phong báo cáo / proposal)