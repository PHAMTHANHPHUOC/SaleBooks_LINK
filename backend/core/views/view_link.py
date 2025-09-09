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
def get_list_links_data(request):
    """
    Trả về danh sách tất cả loại sản phẩm
    """
    loai_list = LinkProfile.objects.all()
    data = []
    for loai in loai_list:
        # Lấy URL tuyệt đối cho ảnh đại diện nếu có
        if loai.anh_dai_dien:
            try:
                anh_url = request.build_absolute_uri(loai.anh_dai_dien.url)
            except Exception:
                anh_url = ""
        else:
            anh_url = ""
        data.append({
            'id': loai.id,
            'name': loai.name,
            'anh_dai_dien': anh_url,
            'links': loai.links,
        })
    return Response({'data': data, 'status': 1})
@api_view(['GET'])
def get_list_links(request):
    """
    Trả về dict:
    {
      "Facebook": {"link": "...", "avatar": "..."},
      "Amazon": {"link": "...", "avatar": "..."}
    }
    """
    profiles = LinkProfile.objects.all()
    data = {}

    for profile in profiles:
        # Lấy link (parse JSON nếu cần)
        link_value = ""
        try:
            if profile.links:
                if isinstance(profile.links, str):
                    try:
                        parsed = json.loads(profile.links)
                        if isinstance(parsed, dict) and "link" in parsed:
                            link_value = parsed["link"]
                        else:
                            link_value = profile.links
                    except json.JSONDecodeError:
                        link_value = profile.links
                else:
                    link_value = profile.links
        except Exception:
            link_value = ""

        # Lấy URL avatar tuyệt đối
        avatar_url = ""
        try:
            if getattr(profile, 'anh_dai_dien', None):
                avatar_url = request.build_absolute_uri(profile.anh_dai_dien.url)
        except Exception:
            avatar_url = ""

        # Gán vào dict
        data[profile.name] = {
            "link": link_value,
            "avatar": avatar_url
        }

    return Response(data)

from django.conf import settings
@require_http_methods(["GET"])
def get_links_api(request):
    try:
        profiles = LinkProfile.objects.all()
        data = {}

        for profile in profiles:
            # Xử lý link
            link_value = ""
            if profile.links:
                if isinstance(profile.links, str):
                    try:
                        parsed_links = json.loads(profile.links)
                        # Nếu links là JSON {"link": "..."} thì lấy key "link"
                        if isinstance(parsed_links, dict) and "link" in parsed_links:
                            link_value = parsed_links["link"]
                        else:
                            link_value = profile.links
                    except json.JSONDecodeError:
                        link_value = profile.links
                else:
                    link_value = profile.links

            # Xử lý avatar
            avatar_url = ""
            if profile.anh_dai_dien:
                try:
                    avatar_url = request.build_absolute_uri(profile.anh_dai_dien.url)
                except Exception:
                    avatar_url = ""

            # Đưa về dict
            data[profile.name] = {
                "link": link_value,
                "avatar": avatar_url
            }

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
        anh_dai_dien = request.FILES.get('anh_dai_dien')  # Lấy file ảnh từ request
        if anh_dai_dien:
            # Kiểm tra kích thước file
            if anh_dai_dien.size > 5 * 1024 * 1024:  # 5MB
                return JsonResponse({'status': False, 'error': 'File quá lớn (>5MB)'}, status=400)
            
            # Kiểm tra định dạng file
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            file_extension = anh_dai_dien.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                return JsonResponse({
                    'status': False, 
                    'error': f'Định dạng file không được hỗ trợ. Chỉ chấp nhận: {", ".join(allowed_extensions)}'
                }, status=400)

        LinkProfile.objects.create(name=name,links=links,anh_dai_dien=anh_dai_dien)
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