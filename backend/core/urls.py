from django.urls import path,re_path
from .views import view_KhachHang



app_name = 'core'

urlpatterns = [
    path('', view_KhachHang.home, name='home'),
    path('login/',view_KhachHang.login),
    path('signup/',view_KhachHang.signup),
    path('check_login/',view_KhachHang.check_login),
    path('quen-mat-khau/',view_KhachHang.quen_mat_khau),
    path('lay-lai-mat-khau/<str:hash_reset>/', view_KhachHang.actionLaylaiMK),
    path('logout/',view_KhachHang.logout),
    path('logout-all/',view_KhachHang.logout_all),
    path('kich-hoat-tai-khoan/<str:hash_active>/', view_KhachHang.kich_hoat_tai_khoan, name='kich_hoat_tai_khoan'),

    



]




