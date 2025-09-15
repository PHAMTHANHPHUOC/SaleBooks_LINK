# Hướng dẫn cài đặt báo cáo tự động Microsoft Teams

## Tổng quan
Hệ thống báo cáo tự động sẽ gửi thống kê hàng ngày về lượt truy cập, người dùng, quốc gia và top sản phẩm vào Microsoft Teams channel.

## Tính năng đã triển khai

### 1. API Endpoints
- `POST /api/teams/send-report/` - Gửi báo cáo thống kê
- `GET /api/teams/preview-report/` - Xem trước báo cáo
- `POST /api/teams/send-custom-report/` - Gửi báo cáo tùy chỉnh

### 2. Giao diện Frontend
- Nút "Gửi báo cáo Teams" trên trang thống kê truy cập
- Nút "Gửi báo cáo Teams" trên trang thống kê sản phẩm
- Chức năng xem trước báo cáo trước khi gửi

### 3. Tự động hóa
- Django management command: `python manage.py send_daily_report`
- Script Python: `python schedule_reports.py`
- Batch script Windows: `send_daily_report.bat`

## Cài đặt và sử dụng

### Bước 1: Cài đặt dependencies
```bash
pip install requests
```

### Bước 2: Cấu hình Microsoft Teams Webhook
URL webhook đã được cấu hình trong code:
```
https://defaultc8a25e62e9734b2ead55aeea08f862.89.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/eafa71ada5c843709d4c3685c58cc8c3/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=o24fzuiefrQEh_NZLCv4KHoV-iWwWF9HbmqB-STtwu0
```

### Bước 3: Test chức năng

#### Test API trực tiếp:
```bash
# Xem trước báo cáo
curl -X GET http://localhost:8000/api/teams/preview-report/

# Gửi báo cáo
curl -X POST http://localhost:8000/api/teams/send-report/
```

#### Test Django command:
```bash
# Test mode (không gửi thực tế)
python manage.py send_daily_report --test

# Gửi thực tế
python manage.py send_daily_report
```

#### Test script Python:
```bash
# Test mode
python schedule_reports.py --test

# Gửi thực tế
python schedule_reports.py
```

### Bước 4: Thiết lập tự động hóa

#### Trên Windows (Task Scheduler):
1. Mở Task Scheduler
2. Tạo task mới
3. Thiết lập trigger: Daily at 18:00
4. Action: Start a program
5. Program: `C:\path\to\your\project\backend\send_daily_report.bat`

#### Trên Linux/Mac (Cron):
```bash
# Mở crontab
crontab -e

# Thêm dòng sau để chạy hàng ngày lúc 18:00
0 18 * * * cd /path/to/your/project/backend && python schedule_reports.py
```

## Nội dung báo cáo

Báo cáo sẽ bao gồm:

### 📊 Thống kê tổng quan
- Tổng lượt truy cập
- Lượt truy cập hôm nay
- Người dùng duy nhất hôm nay
- Số quốc gia truy cập

### 🌍 Top quốc gia truy cập
- Danh sách 5 quốc gia có lượt truy cập cao nhất
- Hiển thị flag emoji và số lượt truy cập

### 🏆 Top sản phẩm hot
- Danh sách 5 sản phẩm được xem nhiều nhất
- Số lượt xem của từng sản phẩm

### ⏰ Thông tin báo cáo
- Thời gian tạo báo cáo
- Nguồn dữ liệu

## Troubleshooting

### Lỗi kết nối
- Kiểm tra URL webhook Microsoft Teams
- Kiểm tra kết nối internet
- Kiểm tra firewall

### Lỗi dữ liệu
- Kiểm tra database có dữ liệu thống kê
- Kiểm tra API endpoints hoạt động
- Xem logs trong Django

### Lỗi permission
- Đảm bảo script có quyền thực thi
- Kiểm tra quyền truy cập file
- Kiểm tra virtual environment

## Monitoring

### Logs
- Django logs: `backend/logs/`
- Application logs: Console output
- Error logs: Django error handling

### Kiểm tra trạng thái
```bash
# Kiểm tra API hoạt động
curl -X GET http://localhost:8000/api/visits/?page=home&include_countries=true

# Kiểm tra database
python manage.py shell
>>> from core.models.VisitCounter import VisitCounter
>>> VisitCounter.objects.all()
```

## Tùy chỉnh

### Thay đổi thời gian gửi báo cáo
- Sửa crontab (Linux/Mac)
- Sửa Task Scheduler (Windows)
- Hoặc thay đổi trong script

### Thay đổi nội dung báo cáo
- Sửa file `backend/core/views/view_teams_report.py`
- Hàm `create_teams_message()`
- Hàm `get_daily_stats()`

### Thêm loại báo cáo mới
- Tạo endpoint mới trong `view_teams_report.py`
- Thêm URL trong `urls.py`
- Tạo management command mới

## Liên hệ hỗ trợ
Nếu gặp vấn đề, vui lòng kiểm tra:
1. Logs hệ thống
2. Kết nối mạng
3. Cấu hình Microsoft Teams
4. Dữ liệu thống kê trong database
