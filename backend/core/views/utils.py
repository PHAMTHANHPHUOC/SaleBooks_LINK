from django.utils import timezone
from django.http import HttpRequest
from ..models import VisitCounter, VisitLog
from datetime import date

def get_client_ip(request):
    """Lấy IP thật của user"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def update_visit_counter(request: HttpRequest, page_name='homepage'):
    """Cập nhật counter và log visit"""
    
    # Lấy hoặc tạo counter record
    counter, created = VisitCounter.objects.get_or_create(
        page_name=page_name,
        defaults={
            'total_visits': 0,
            'today_visits': 0,
            'last_visit_date': timezone.now().date()
        }
    )
    
    # Kiểm tra ngày mới
    today = timezone.now().date()
    if counter.last_visit_date < today:
        counter.today_visits = 0
        counter.last_visit_date = today
    
    # Tăng counter
    counter.total_visits += 1
    counter.today_visits += 1
    counter.save()
    
    # Log visit (optional - để tracking chi tiết)
    VisitLog.objects.create(
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        page_visited=page_name,
    )
    return 


def get_visit_stats(page_name='homepage'):
    """Lấy thống kê visit"""
    try:
        counter = VisitCounter.objects.get(page_name=page_name)
        
        # Thống kê tuần này
        from datetime import datetime, timedelta
        week_start = timezone.now().date() - timedelta(days=timezone.now().weekday())
        week_visits = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date__gte=week_start
        ).count()
        
        # Thống kê tháng này
        month_start = timezone.now().replace(day=1).date()
        month_visits = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date__gte=month_start
        ).count()
        
        return {
            'total_visits': counter.total_visits,
            'today_visits': counter.today_visits,
            'week_visits': week_visits,
            'month_visits': month_visits,
            'last_update': counter.updated_at,
        }
    except VisitCounter.DoesNotExist:
        return {
            'total_visits': 0,
            'today_visits': 0,
            'week_visits': 0,
            'month_visits': 0,
            'last_update': None,
        }