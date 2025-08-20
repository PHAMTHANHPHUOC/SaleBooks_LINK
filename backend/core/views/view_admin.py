from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from core.models import KhachHang
from django.contrib.auth import authenticate

@api_view(['POST'])
@csrf_exempt
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        return Response({
            'message': 'Đăng nhập thành công!',
            'status': 1
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'message': 'Tài khoản hoặc mật khẩu không đúng!',
            'status': 0
        }, status=status.HTTP_401_UNAUTHORIZED)
           


