from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from core.models.LinkMangXaHoi import LinkProfile
from django.views.decorators.http import require_http_methods
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_list_links(request):
    """
    Trả về danh sách tất cả loại sản phẩm
    """
    loai_list = LinkProfile.objects.all()
    data = []
    for loai in loai_list:
        data.append({
            'id': loai.id,
            'name': loai.name,
            'links': loai.links,  # Thêm trường link_danh_muc
           
        })
    return Response(data)

@require_http_methods(["GET"])
def get_links_api(request):
    try:
        profiles = LinkProfile.objects.all()
        data = {}
        
        for profile in profiles:
            try:
                # Thử parse JSON
                if profile.links:
                    if isinstance(profile.links, str):
                        # Nếu là string, thử parse JSON
                        try:
                            parsed_links = json.loads(profile.links)
                            data[profile.name] = parsed_links
                        except json.JSONDecodeError:
                            # Nếu không phải JSON, dùng raw string
                            data[profile.name] = profile.links
                    else:
                        data[profile.name] = profile.links
                else:
                    data[profile.name] = ""
            except Exception as e:
                print(f"Error processing profile {profile.name}: {e}")
                data[profile.name] = ""
        
        return JsonResponse({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['POST'])
def create_link(request):
    try:
        name = request.data.get('name')
        links = request.data.get('links', '')  # Mặc định là rỗng nếu không có

        LinkProfile.objects.create(name=name,links=links)
        return JsonResponse({'status': True, 'message': 'thêm link thành công.'})
    except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)}, status=400)
        
@api_view(['POST'])
def delete_link(request, id):
    try:
        LinkProfile.objects.get(id=id).delete()
        return Response({'status': True, 'message': 'Đã xóa thành công'})
    except LinkProfile.DoesNotExist:
        return Response({'status': False, 'message': 'Không tìm thấy link'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])  
def update_link(request, id):
    try:
        data = LinkProfile.objects.get(id=id)
        data.links = request.data.get('links')  
        data.save()
        return Response({
            'status': True,
            'message': 'Đã cập nhật link thành công!'
        }, status=status.HTTP_200_OK)
    except LinkProfile.DoesNotExist:
        return Response({
            'status': False,
            'message': 'Không tìm được link để cập nhật!'
        }, status=status.HTTP_404_NOT_FOUND)