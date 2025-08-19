from django.urls import path,re_path
from .views import view_count


app_name = 'core'

urlpatterns = [
path('', view_count.homepage, name='homepage'),
path('book/<int:book_id>/', view_count.coloring_book_detail, name='book_detail'),
path('api/visits/', view_count.get_visit_count_api, name='visit_api'),


    



]




