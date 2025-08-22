
from core.models.SanPham import SanPham,LoaiSanPham,SanPhamView
from django.shortcuts import get_object_or_404
from core.serializers import SanPhamSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework import status
from rest_framework.decorators import api_view
import logging
from datetime import timedelta
from django.db.models import Count
from django.utils.timezone import now

logger = logging.getLogger(__name__)



@require_GET
def top_san_pham(request):
    loai = request.GET.get("loai", "ngay")  # giá trị: "ngay", "thang", "nam"
    today = now().date()

    if loai == "ngay":
        start = today
    elif loai == "tuan":
        # Lấy ngày đầu tuần (theo ISO: thứ 2)
        start = today - timedelta(days=today.weekday())
    elif loai == "thang":
        start = today.replace(day=1)
    elif loai == "nam":
        start = today.replace(month=1, day=1)
    else:
        return JsonResponse({"error": "Tham số 'loai' không hợp lệ"}, status=400)

    views = (
        SanPhamView.objects.filter(created_at__date__gte=start)
        .values("san_pham__id", "san_pham__ten_san_pham", "san_pham__anh_dai_dien")
        .annotate(so_luot=Count("id"))
        .order_by("-so_luot")[:10]
    )
    data = [
        {
            "id": v["san_pham__id"],
            "ten": v["san_pham__ten_san_pham"],
            "anh": v["san_pham__anh_dai_dien"],
            "so_luot": v["so_luot"]
        }
        for v in views
    ]
    return JsonResponse(data, safe=False)


@api_view(['POST'])
def tang_luot_xem(request, pk):
    if request.method == "POST":
        sp = get_object_or_404(SanPham, pk=pk)
        SanPhamView.objects.create(san_pham=sp)
        return JsonResponse({
            "success": True,
            "message": f"Đã ghi nhận click cho sản phẩm {sp.ten_san_pham}"
        })
    return JsonResponse({"success": False}, status=400)



@api_view(['POST'])
def change_san_pham(request):
    """
    Thay đổi trạng thái của loại sản phẩm
    """
    try:
        loai = SanPham.objects.get(id=request.data.get('id'))
        loai.tinh_trang = not bool(loai.tinh_trang)
        loai.save()
        return Response({
            'status': True,
            'message': f"Đã đổi tình trạng {loai.ten_san_pham} thành công"
        }, status=status.HTTP_200_OK)
    except SanPham.DoesNotExist:
        return Response({
            'status': False,
            'message': 'Không tìm thấy loại sản phẩm'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def create_san_pham(request):
    try:
        ten_san_pham = request.data.get('ten_san_pham')
        duong_dan_ngoai = request.data.get('duong_dan_ngoai')  # Mặc định là 0 nếu không 
        gia_mac_dinh = request.data.get('gia_mac_dinh')  # Mặc định là 0 nếu không có
        anh_dai_dien = request.data.get('anh_dai_dien')  #
        tinh_trang = request.data.get('tinh_trang', 0)  # Mặc định là 0 nếu không có
        loai_san_pham_id = request.data.get('loai_san_pham')  # Mặc định là 0 nếu không có
        loai_san_pham = LoaiSanPham.objects.get(id=loai_san_pham_id) if loai_san_pham_id else None        
        
        SanPham.objects.create(
            ten_san_pham=ten_san_pham,
            duong_dan_ngoai=duong_dan_ngoai,
            gia_mac_dinh=gia_mac_dinh,
            anh_dai_dien=anh_dai_dien,
            tinh_trang=tinh_trang,
            loai_san_pham=loai_san_pham
        )
        return JsonResponse({'status': True, 'message': 'thêm loại sản phẩm thành công.'})
    except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)}, status=400)
@api_view(['POST'])
def delete_san_pham(request, id):
    try:
        loai = SanPham.objects.get(id=id)
        loai.delete()
        return Response({'status': True,'message': 'Đã xóa thành công'})
    except SanPham.DoesNotExist:
        return Response({'status': False,'message': 'Không tìm thấy loại sản phẩm'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])  
def update_san_pham(request, id):
    try:
        data = SanPham.objects.get(id=id)
        data.ten_san_pham = request.data.get('ten_san_pham')
        data.duong_dan_ngoai = request.data.get('duong_dan_ngoai')
        data.gia_mac_dinh = request.data.get('gia_mac_dinh')
        data.tinh_trang = request.data.get('tinh_trang', 0)  # Mặc định là 0 nếu không có
        data.anh_dai_dien = request.data.get('anh_dai_dien')
        data.loai_san_pham_id = request.data.get('loai_san_pham')  # Cập nhật loại sản phẩm nếu có
        data.save()
        return Response({
            'status': True,
            'message': 'Đã cập nhật loại sản phẩm thành công!'
        }, status=status.HTTP_200_OK)
    except SanPham.DoesNotExist:
        return Response({
            'status': False,
            'message': 'Không tìm được sản phẩm để cập nhật!'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def change_loai_san_pham(request):
    """
    Thay đổi trạng thái của loại sản phẩm
    """
    try:
        loai = LoaiSanPham.objects.get(id=request.data.get('id'))
        loai.tinh_trang = not bool(loai.tinh_trang)
        loai.save()
        return Response({
            'status': True,
            'message': f"Đã đổi tình trạng {loai.ten_loai} thành công"
        }, status=status.HTTP_200_OK)
    except LoaiSanPham.DoesNotExist:
        return Response({
            'status': False,
            'message': 'Không tìm thấy loại sản phẩm'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
       

@api_view(['POST'])
def create_loai_san_pham(request):
    try:
        ten_loai = request.data.get('ten_loai')
        link_danh_muc = request.data.get('link_danh_muc', '')  # Mặc định là rỗng nếu không có
        tinh_trang = request.data.get('tinh_trang')  # Mặc định là 0 nếu không có
        LoaiSanPham.objects.create(ten_loai=ten_loai,  tinh_trang=tinh_trang,link_danh_muc=link_danh_muc)
        return JsonResponse({'status': True, 'message': 'thêm loại sản phẩm thành công.'})
    except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)}, status=400)
@api_view(['POST'])  
def update_loai_san_pham(request, id):
    try:
        data = LoaiSanPham.objects.get(id=id)
        data.ten_loai = request.data.get('ten_loai')
        data.link_danh_muc = request.data.get('link_danh_muc', '')  # Cập nhật link danh mục nếu có
        data.tinh_trang = request.data.get('tinh_trang')  # Cập nhật trạng thái nếu có
        data.save()
        return Response({
            'status': True,
            'message': 'Đã cập nhật loại sản phẩm thành công!'
        }, status=status.HTTP_200_OK)
    except LoaiSanPham.DoesNotExist:
        return Response({
            'status': False,
            'message': 'Không tìm được sản phẩm để cập nhật!'
        }, status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
def delete_loai_san_pham(request, id):
    try:
        loai = LoaiSanPham.objects.get(id=id)
        loai.delete()
        return Response({'status': True,'message': 'Đã xóa thành công'})
    except LoaiSanPham.DoesNotExist:
        return Response({'status': False,'message': 'Không tìm thấy loại sản phẩm'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def product_data(request):
    """
    Trả về dữ liệu sản phẩm cho trang chủ
    """
    try:
        # Giả sử bạn có một mô hình Sản Phẩm
        san_phams = SanPham.objects.all()  # Thay thế bằng mô hình thực tế của bạn

        # san_phams = SanPham.objects.filter(loai_san_pham_id=id, loai_san_pham__tinh_trang=1)
        serializer = SanPhamSerializer(san_phams, many=True)
        return Response({
            'status': True,
            'data': serializer.data
        })
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu sản phẩm: {str(e)}")
        return Response({
            'status': False,
            'message': "Lỗi khi lấy dữ liệu sản phẩm"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def product_type(request, id):
    """
    Trả về dữ liệu sản phẩm theo loại
    """
    try:
        san_phams = SanPham.objects.filter(loai_san_pham_id=id, tinh_trang=1)
        serializer = SanPhamSerializer(san_phams, many=True)
        return Response({
            'status': True,
            'data': serializer.data
        })
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu sản phẩm theo loại: {str(e)}")
        return Response({
            'status': False,
            'message': "Lỗi khi lấy dữ liệu sản phẩm theo loại"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def product_data_type(request):
    """
    Trả về danh sách tất cả loại sản phẩm
    """
    loai_list = LoaiSanPham.objects.all()
    data = []
    for loai in loai_list:
        data.append({
            'id': loai.id,
            'ten_loai': loai.ten_loai,
            'link_danh_muc': loai.link_danh_muc,  # Thêm trường link_danh_muc
            'tinh_trang': loai.tinh_trang,
        })
    return Response(data)