
# from core.models.SanPham import SanPham
# from core.serializers import SanPhamSerializer
# from rest_framework.response import Response
# from rest_framework import status
# import logging
# logger = logging.getLogger(__name__)
# def product_data(request):
#     """
#     Trả về dữ liệu sản phẩm cho trang chủ
#     """
#     try:
#         # Giả sử bạn có một mô hình Sản Phẩm
#         san_phams = SanPham.objects.all()  # Thay thế bằng mô hình thực tế của bạn
#         serializer = SanPhamSerializer(san_phams, many=True)
#         return Response({
#             'status': True,
#             'data': serializer.data
#         })
#     except Exception as e:
#         logger.error(f"Lỗi khi lấy dữ liệu sản phẩm: {str(e)}")
#         return Response({
#             'status': False,
#             'message': "Lỗi khi lấy dữ liệu sản phẩm"
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# def product_type(request, id):
#     """
#     Trả về dữ liệu sản phẩm theo loại
#     """
#     try:
#         san_phams = SanPham.objects.filter(type_id=id)  # Thay thế bằng trường loại thực tế của bạn
#         serializer = SanPhamSerializer(san_phams, many=True)
#         return Response({
#             'status': True,
#             'data': serializer.data
#         })
#     except Exception as e:
#         logger.error(f"Lỗi khi lấy dữ liệu sản phẩm theo loại: {str(e)}")
#         return Response({
#             'status': False,
#             'message': "Lỗi khi lấy dữ liệu sản phẩm theo loại"
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)