from django.shortcuts import render
from django.http import JsonResponse
from .utils import update_visit_counter, get_visit_stats


def homepage(request):
    """API tính lượt truy cập cho trang frontend http://localhost:5173/"""
    counter = update_visit_counter(request, 'frontend_home')
    stats = get_visit_stats('frontend_home')
    return JsonResponse(stats)

def get_visit_count_api(request):
    """API trả về số lượt visit (cho AJAX)"""
    page_name = request.GET.get('page', 'homepage')
    stats = get_visit_stats(page_name)
    return JsonResponse(stats)

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