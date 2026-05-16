# AI Lead Scoring & Automation System (Bất Động Sản)

Hệ thống tự động hóa lấy dữ liệu từ Google Sheets, chấm điểm tiềm năng khách hàng bằng AI (Rule-based) và hỗ trợ kiểm duyệt (Human-in-the-loop) trước khi xuất file bàn giao.

## 🌟 Tính năng chính
- **Kết nối Google Sheets**: Tự động đồng bộ dữ liệu khách hàng.
- **Engine Chấm điểm**: Phân loại khách hàng dựa trên bộ quy tắc nghiệp vụ (Ngân sách, Vị trí, Loại hình, Spam...).
- **Giao diện Kiểm duyệt**: Cho phép con người chỉnh sửa kết quả trực tiếp trước khi chốt.
- **Xuất dữ liệu**: Hỗ trợ xuất file Excel chuẩn để bàn giao cho đội ngũ Sales.

## 🛠 Cấu trúc dự án
- `app_lead_scoring.py`: Mã nguồn chính của ứng dụng Streamlit.
- `requirements.txt`: Danh sách các thư viện cần thiết.
- `lead_scoring_skill.md`: Mô tả chi tiết kỹ năng và logic chấm điểm.
- `run_scoring.py`: Script chạy nhanh bằng Python (không cần giao diện).

## 🚀 Hướng dẫn cài đặt và chạy

### 1. Cài đặt môi trường
Đảm bảo bạn đã cài đặt Python 3.8 trở lên.
```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng giao diện (Streamlit)
```bash
streamlit run app_lead_scoring.py
```

### 3. Hướng dẫn sử dụng
1. Mở ứng dụng trên trình duyệt.
2. Nhấn nút **Process Leads** để hệ thống bắt đầu phân tích.
3. Kiểm tra kết quả trong bảng, bạn có thể sửa trực tiếp Điểm hoặc Phân loại.
4. Nhấn **Tải xuống file Excel** để nhận file kết quả cuối cùng.

## 📁 Hướng dẫn đưa lên GitHub
1. Tạo một Repository mới trên GitHub.
2. Chạy các lệnh sau tại thư mục dự án:
```bash
git init
git add .
git commit -m "Initial commit: AI Lead Scoring System"
git branch -M main
git remote add origin <LINK_REPOSITORY_CUA_BAN>
git push -u origin main
```

---
© 2026 AI Lead Scoring System - Phát triển cho mục tiêu chuyên nghiệp hóa ngành Bất động sản.
