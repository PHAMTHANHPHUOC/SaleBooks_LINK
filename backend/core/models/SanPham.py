from django.db import models

# Bảng loại sản phẩm
class LoaiSanPham(models.Model):
    ten_loai = models.CharField(max_length=100, unique=True)  # Tên loại sản phẩm
    tinh_trang = models.IntegerField(default=0)
    # Mô tả loại sản phẩm (tuỳ chọn)
    
    def __str__(self):
        return self.ten_loai


# Bảng sản phẩm
class SanPham(models.Model):
    ten_san_pham = models.CharField(max_length=255)   
    duong_dan_ngoai = models.URLField(blank=True, null=True)  
    gia_mac_dinh = models.BigIntegerField() 
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
