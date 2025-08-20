from django.urls import path,re_path
from .views import view_count,view_sanpham,view_admin



app_name = 'core'

urlpatterns = [
path('', view_count.homepage, name='homepage'),
path('book/<int:book_id>/', view_count.coloring_book_detail, name='book_detail'),
path('api/visits/', view_count.get_visit_count_api, name='visit_api'),
path('api/frontend-page-visit/', view_count.frontend_page_visit, name='frontend_page_visit'),


path('products/data/', view_sanpham.product_data, name='product_data'),
path('products/create/', view_sanpham.create_san_pham, name='create_loai_san_pham'),
path('products/update/<int:id>/', view_sanpham.update_san_pham, name='update_san_pham'),
path('products/delete/<int:id>/', view_sanpham.delete_san_pham, name='delete_san_pham'),






path('products/type/<int:id>/', view_sanpham.product_type, name='product_list_by_type'),
path('products/type/list/', view_sanpham.product_data_type, name='product_list_all'),
path('products/type/create/', view_sanpham.create_loai_san_pham, name='create_loai_san_pham'),
path('products/type/update/<int:id>/', view_sanpham.update_loai_san_pham, name='update_loai_san_pham'),
path('products/type/delete/<int:id>/', view_sanpham.delete_loai_san_pham, name='delete_loai_san_pham'),
path('products/type/change-status/', view_sanpham.change_loai_san_pham, name='change_loai_san_pham'),


    


path('admin/login/',view_admin.admin_login,name='admin_login'),






    



]




