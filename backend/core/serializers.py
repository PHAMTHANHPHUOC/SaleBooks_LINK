from rest_framework import serializers
from core.models.SanPham import SanPham
class SanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanPham
        fields = '__all__'  