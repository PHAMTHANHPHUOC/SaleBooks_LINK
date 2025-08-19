from rest_framework import serializers
from .models import SanPham
class SanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanPham
        fields = '__all__'  