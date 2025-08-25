from rest_framework import serializers
from core.models.SanPham import SanPham
class SanPhamSerializer(serializers.ModelSerializer):
    gia_mac_dinh = serializers.CharField() 
    class Meta:
        model = SanPham
        fields = '__all__'  