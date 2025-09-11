from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from core.models.StyleConfig import StyleConfig
from django.views.decorators.http import require_http_methods
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_list_styles(request):
    """
    Trả về danh sách tất cả loại sản phẩm
    """
    list_data = StyleConfig.objects.all()
    data = []
    for loai in list_data:
        data.append({
            'id': loai.id,
            'tag': loai.tag,
            'font_family': loai.font_family,  # Thêm trường link_danh_muc
            'font_size': loai.font_size,
            'color': loai.color,
            'background': loai.background,
        })
    return Response(data)

@api_view(['GET'])
def get_data_styles(request):
    """
    Trả về danh sách tất cả loại sản phẩm dưới dạng dict {tag: {...style...}}
    """
    list_data = StyleConfig.objects.all()
    data = {}
    for loai in list_data:
        data[loai.tag] = {
            'font_family': loai.font_family,
            'font_size': loai.font_size,
            'color': loai.color,
            'background': loai.background,
        }
    return Response(data)

@api_view(['POST'])
def create_styles(request):
    try:
        tag = request.data.get('tag')
        font_family = request.data.get('font_family', '')  
        font_size = request.data.get('font_size', '')  
        color = request.data.get('color', '')  
        background = request.data.get('background', '')  
        StyleConfig.objects.create(tag=tag,font_family=font_family,font_size=font_size,color=color,background=background)
        return JsonResponse({'status': True, 'message': 'thêm tag thành công.'})
    except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)}, status=400)

@api_view(['POST'])
def delete_styles(request, id):
    try:
        StyleConfig.objects.get(id=id).delete()
        return Response({'status': True, 'message': 'Đã xóa thành công'})
    except StyleConfig.DoesNotExist:
        return Response({'status': False, 'message': 'Không tìm thấy tag'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])  
def update_styles(request, id):
    try:
        data = StyleConfig.objects.get(id=id)
        data.tag = request.data.get('tag', data.tag)
        data.font_family = request.data.get('font_family', data.font_family)
        data.font_size = request.data.get('font_size', data.font_size)
        data.color = request.data.get('color', data.color)
        data.background = request.data.get('background', data.background)


        # Xử lý cập nhật ảnh đại diện nếu có file mới

        data.save()
        return Response({
            'status': True,
            'message': 'Đã cập nhật link thành công!'
        }, status=status.HTTP_200_OK)
    except StyleConfig.DoesNotExist:
        return Response({
            'status': False,
            'message': 'Không tìm được link để cập nhật!'
        }, status=status.HTTP_404_NOT_FOUND)