# from django.shortcuts import render
# from django.http import JsonResponse
# from .utils import update_visit_counter, get_visit_stats

# def homepage(request):
#     """Homepage với counter"""
#     # Cập nhật counter
#     counter = update_visit_counter(request, 'homepage')
    
#     # Lấy thống kê
#     stats = get_visit_stats('homepage')
    
#     context = {
#         'visit_stats': stats,
#         'page_title': 'Coloring Book Store'
#     }
#     return render(request,'core/home.html')

# def get_visit_count_api(request):
#     """API trả về số lượt visit (cho AJAX)"""
#     page_name = request.GET.get('page', 'homepage')
#     stats = get_visit_stats(page_name)
#     return JsonResponse(stats)

# def coloring_book_detail(request, book_id):
#     """Chi tiết sách - có counter riêng"""
#     page_name = f'book_{book_id}'
#     counter = update_visit_counter(request, page_name)
#     stats = get_visit_stats(page_name)
    
#     context = {
#         'book_id': book_id,
#         'visit_stats': stats,
#     }
#     return render(request, 'book_detail.html', context)