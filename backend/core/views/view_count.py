from django.shortcuts import render
from django.http import JsonResponse
from .utils import update_visit_counter, get_visit_stats,calculate_growth_rate
 # Lấy thêm dữ liệu khác
from datetime import datetime, timedelta
from django.db.models import Count
from core.models.VisitCounter import VisitLog, VisitCounter

def homepage(request):
    """API tính lượt truy cập cho trang frontend http://localhost:5173/"""
    counter = update_visit_counter(request, 'frontend_home')
    stats = get_visit_stats('frontend_home')
    return JsonResponse(stats)

def get_visit_count_api(request):
    """API trả về đầy đủ dữ liệu cho frontend"""
    page_name = request.GET.get('page', 'home')
    stats = get_visit_stats(page_name)
    
   
    
    # Thống kê theo giờ (24h qua)
    hourly_stats = []
    now = datetime.now()
    for i in range(24):
        hour_start = now - timedelta(hours=i+1)
        hour_end = now - timedelta(hours=i)
        count = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__range=[hour_start, hour_end]
        ).count()
        hourly_stats.append({
            'hour': hour_start.strftime('%H:00'),
            'visits': count
        })
    
    # Top pages được truy cập nhiều nhất
    top_pages = VisitCounter.objects.order_by('-total_visits')[:5].values(
        'page_name', 'total_visits', 'today_visits'
    )
    
    # Thống kê theo ngày (7 ngày qua)
    daily_stats = []
    for i in range(7):
        date_check = now.date() - timedelta(days=i)
        count = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date=date_check
        ).count()
        daily_stats.append({
            'date': date_check.strftime('%d/%m'),
            'visits': count
        })
    
    # Unique visitors (theo IP) hôm nay
    unique_today = VisitLog.objects.filter(
        page_visited=page_name,
        visit_time__date=now.date()
    ).values('ip_address').distinct().count()
    
    # Browser stats
    from collections import Counter
    user_agents = VisitLog.objects.filter(
        page_visited=page_name,
        visit_time__gte=now - timedelta(days=7)
    ).values_list('user_agent', flat=True)
    
    browser_stats = []
    for agent in user_agents[:50]:  # Lấy 50 record gần nhất
        if 'Chrome' in agent:
            browser_stats.append('Chrome')
        elif 'Firefox' in agent:
            browser_stats.append('Firefox')
        elif 'Safari' in agent:
            browser_stats.append('Safari')
        elif 'Edge' in agent:
            browser_stats.append('Edge')
        else:
            browser_stats.append('Other')
    
    browser_count = dict(Counter(browser_stats))
    
    # Kết quả đầy đủ
    result = {
        # Visit counters cơ bản
        'total_visits': int(stats.get('total_visits', 0)),
        'today_visits': int(stats.get('today_visits', 0)),
        'week_visits': int(stats.get('week_visits', 0)),
        'month_visits': int(stats.get('month_visits', 0)),
        'unique_today': unique_today,
        'last_update': stats.get('last_update').strftime('%Y-%m-%dT%H:%M:%S') if stats.get('last_update') else '',
        
        # Thống kê chi tiết
        'hourly_stats': hourly_stats[:12],  # 12h gần nhất
        'daily_stats': list(reversed(daily_stats)),  # 7 ngày, mới nhất trước
        'top_pages': list(top_pages),
        'browser_stats': browser_count,
        
        # Metadata
        'page_name': page_name,
        'server_time': now.strftime('%Y-%m-%dT%H:%M:%S'),
        'timezone': 'UTC+7',
        
        # Growth rates
        'growth': {
            'today_vs_yesterday': calculate_growth_rate(page_name, 'day'),
            'this_week_vs_last_week': calculate_growth_rate(page_name, 'week'),
            'this_month_vs_last_month': calculate_growth_rate(page_name, 'month'),
        }
    }
    
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

def coloring_book_detail(request, book_id):
    """Chi tiết sách - có counter riêng"""
    page_name = f'book_{book_id}'
    counter = update_visit_counter(request, page_name)
    stats = get_visit_stats(page_name)
    
    context = {
        'book_id': book_id,
        'visit_stats': stats,
    }
    return render(request, 'book_detail.html', context)

def frontend_page_visit(request):
    """API tính và trả về lượt truy cập cho bất kỳ trang frontend nào (dùng query param 'page')"""
    page_name = request.GET.get('page', 'frontend_home')
    counter = update_visit_counter(request, page_name)
    stats = get_visit_stats(page_name)
    return JsonResponse(stats)