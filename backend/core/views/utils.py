from django.utils import timezone
from django.http import HttpRequest
from ..models import VisitCounter, VisitLog
from datetime import date
from datetime import datetime, timedelta
from django.db.models import Count
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


def calculate_growth_rate(page_name, period):
    """Tính tỷ lệ tăng trưởng"""
    from datetime import datetime, timedelta
    now = datetime.now()
    
    if period == 'day':
        current_start = now.date()
        previous_start = current_start - timedelta(days=1)
        current_count = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date=current_start
        ).count()
        previous_count = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date=previous_start
        ).count()
        
    elif period == 'week':
        current_start = now.date() - timedelta(days=now.weekday())
        previous_start = current_start - timedelta(days=7)
        current_count = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date__gte=current_start
        ).count()
        previous_count = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date__gte=previous_start,
            visit_time__date__lt=current_start
        ).count()
        
    elif period == 'month':
        current_start = now.replace(day=1).date()
        if current_start.month == 1:
            previous_start = current_start.replace(year=current_start.year-1, month=12)
        else:
            previous_start = current_start.replace(month=current_start.month-1)
        
        current_count = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date__gte=current_start
        ).count()
        previous_count = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date__gte=previous_start,
            visit_time__date__lt=current_start
        ).count()
    
    if previous_count == 0:
        return 100 if current_count > 0 else 0
    
    growth = ((current_count - previous_count) / previous_count) * 100
    return round(growth, 1)
def get_visit_stats(page_name='homepage'):
    """Lấy thống kê visit"""
    try:
        counter = VisitCounter.objects.get(page_name=page_name)
        print(f"[DEBUG] Found counter: {counter.page_name} - Total: {counter.total_visits}")
        
        # Force refresh từ DB
        counter.refresh_from_db()
        
        # Thống kê tuần này
        from datetime import datetime, timedelta
        week_start = timezone.now().date() - timedelta(days=timezone.now().weekday())
        week_visits = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date__gte=week_start
        ).count()
        print(f"[DEBUG] Week visits query: {week_visits}")
        
        # Thống kê tháng này
        month_start = timezone.now().replace(day=1).date()
        month_visits = VisitLog.objects.filter(
            page_visited=page_name,
            visit_time__date__gte=month_start
        ).count()
        print(f"[DEBUG] Month visits query: {month_visits}")
        
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
def get_client_ip(request):
    """Lấy IP thật của user"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def update_visit_counter_from_data(page_name):
    """Cập nhật counter không cần request object"""
    from django.utils import timezone
    
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
    
    return counter

def get_country_stats(page_name):
    """Lấy thống kê theo quốc gia cho các khoảng thời gian"""
    from django.utils import timezone
    now = timezone.now()
    
    def get_period_stats(period):
        if period == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = VisitLog.objects.filter(
                page_visited=page_name,
                visit_time__gte=start_date
            )
        elif period == 'week':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = VisitLog.objects.filter(
                page_visited=page_name,
                visit_time__gte=start_date
            )
        elif period == 'month':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            queryset = VisitLog.objects.filter(
                page_visited=page_name,
                visit_time__gte=start_date
            )
        else:  # all
            queryset = VisitLog.objects.filter(page_visited=page_name)
        
        # Group by country và đếm
        stats = queryset.values('country_code', 'country_name').annotate(
            visits=Count('id')
        ).exclude(
            country_code__isnull=True
        ).order_by('-visits')
        
        return list(stats)
    
    return {
        'today': get_period_stats('today'),
        'week': get_period_stats('week'),
        'month': get_period_stats('month'),
        'all': get_period_stats('all')
    }