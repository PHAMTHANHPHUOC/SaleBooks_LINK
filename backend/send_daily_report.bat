@echo off
REM Script tự động gửi báo cáo thống kê hàng ngày
REM Có thể chạy với Windows Task Scheduler

echo ========================================
echo    BÁO CÁO THỐNG KÊ HÀNG NGÀY
echo ========================================
echo Thời gian: %date% %time%
echo.

REM Chuyển đến thư mục backend
cd /d "%~dp0"

REM Kích hoạt virtual environment (nếu có)
if exist "venv\Scripts\activate.bat" (
    echo Đang kích hoạt virtual environment...
    call venv\Scripts\activate.bat
)

REM Chạy script gửi báo cáo
echo Đang gửi báo cáo thống kê...
python schedule_reports.py

REM Kiểm tra kết quả
if %errorlevel% equ 0 (
    echo.
    echo ✅ Báo cáo đã được gửi thành công!
) else (
    echo.
    echo ❌ Có lỗi xảy ra khi gửi báo cáo!
)

echo.
echo ========================================
echo Hoàn thành lúc: %date% %time%
echo ========================================

REM Tạm dừng để xem kết quả (có thể bỏ dòng này khi chạy tự động)
pause
