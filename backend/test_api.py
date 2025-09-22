#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, time, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models.SanPham import SanPhamView
from django.utils.timezone import now

def test_date_ranges():
    today = now().date()
    print(f"Today: {today}")
    
    # Test các khoảng thời gian
    test_cases = [
        ("ngay", "Hôm nay"),
        ("tuan", "Tuần này"), 
        ("thang", "Tháng này"),
        ("nam", "Năm này")
    ]
    
    for loai, label in test_cases:
        print(f"\n=== {label} ({loai}) ===")
        
        if loai == "ngay":
            start = datetime.combine(today, time.min)
            end = datetime.combine(today, time.max)
        elif loai == "tuan":
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
            start = datetime.combine(start_date, time.min)
            end = datetime.combine(end_date, time.max)
        elif loai == "thang":
            start_date = today.replace(day=1)
            if today.month == 12:
                end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
            start = datetime.combine(start_date, time.min)
            end = datetime.combine(end_date, time.max)
        elif loai == "nam":
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
            start = datetime.combine(start_date, time.min)
            end = datetime.combine(end_date, time.max)
        
        print(f"Start: {start}")
        print(f"End: {end}")
        
        # Đếm records
        count = SanPhamView.objects.filter(
            created_at__gte=start,
            created_at__lte=end
        ).count()
        
        print(f"Found {count} records")
        
        # Lấy top products
        views = (
            SanPhamView.objects.filter(
                created_at__gte=start,
                created_at__lte=end
            )
            .values("san_pham__id", "san_pham__ten_san_pham", "san_pham__anh_dai_dien")
            .annotate(so_luot=Count("id"))
            .order_by("-so_luot")[:10]
        )
        
        print(f"Top products:")
        for v in views:
            print(f"  - {v['san_pham__ten_san_pham']}: {v['so_luot']} views")

if __name__ == "__main__":
    from django.db.models import Count
    test_date_ranges()
