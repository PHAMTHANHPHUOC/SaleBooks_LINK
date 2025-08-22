from django.db import models
from django.utils import timezone

# Bảng loại sản phẩm
class LoaiSanPham(models.Model):
    ten_loai = models.CharField(max_length=100, unique=True)  # Tên loại sản phẩm
    tinh_trang = models.IntegerField(default=0)
    link_danh_muc = models.URLField(blank=True, null=True)  
    
    # Mô tả loại sản phẩm (tuỳ chọn)
    
    def __str__(self):
        return self.ten_loai


# Bảng sản phẩm
class SanPham(models.Model):
    ten_san_pham = models.CharField(max_length=255)   
    duong_dan_ngoai = models.URLField(blank=True, null=True)  
    gia_mac_dinh = models.BigIntegerField()
    tinh_trang = models.IntegerField(default=0)
     
    anh_dai_dien = models.URLField(max_length=500, blank=True, null=True) 
    
    # Thêm ForeignKey tới LoaiSanPham
    loai_san_pham = models.ForeignKey(
        LoaiSanPham,
        on_delete=models.SET_NULL,   # Nếu loại bị xóa, sản phẩm vẫn giữ nhưng loai_san_pham = NULL
        null=True,
        blank=True,
        related_name='san_phams'    # Có thể dùng: loai_san_pham.san_phams.all()
    )

    def __str__(self):
        return self.ten_san_pham

class SanPhamView(models.Model):
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        related_name="views"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.san_pham.ten_san_pham} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"