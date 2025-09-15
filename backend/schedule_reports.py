#!/usr/bin/env python3
"""
Script tự động gửi báo cáo thống kê vào Microsoft Teams
Có thể chạy với cron job hoặc Windows Task Scheduler

Cách sử dụng:
1. Chạy hàng ngày lúc 18:00: python schedule_reports.py
2. Chạy test: python schedule_reports.py --test
3. Chạy với thời gian cụ thể: python schedule_reports.py --time 18:00
"""

import os
import sys
import django
import argparse
from datetime import datetime

# Thêm đường dẫn Django project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Thiết lập Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

def main():
    parser = argparse.ArgumentParser(description='Gửi báo cáo thống kê tự động')
    parser.add_argument('--test', action='store_true', help='Chạy ở chế độ test')
    parser.add_argument('--time', type=str, help='Thời gian gửi báo cáo (HH:MM)')
    
    args = parser.parse_args()
    
    print(f"🕐 Thời gian chạy: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Gọi Django management command
        call_command('send_daily_report', test=args.test, time=args.time)
        print("✅ Hoàn thành gửi báo cáo")
        
    except Exception as e:
        print(f"❌ Lỗi khi gửi báo cáo: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
