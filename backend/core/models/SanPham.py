from django.db import models

# Bảng loại sản phẩm
class LoaiSanPham(models.Model):
    ten_loai = models.CharField(max_length=100, unique=True)  # Tên loại sản phẩm
    mo_ta = models.TextField(blank=True, null=True)           # Mô tả loại sản phẩm (tuỳ chọn)
    
    def __str__(self):
        return self.ten_loai


# Bảng sản phẩm
class SanPham(models.Model):
    ma_san_pham = models.CharField(max_length=50, unique=True)  
    ten_san_pham = models.CharField(max_length=255)  
    mo_ta = models.TextField()  
    so_trang = models.IntegerField(blank=True, null=True)  
    kich_thuoc = models.CharField(max_length=100, blank=True)  
    loai_bia = models.CharField(max_length=50, blank=True)  
    duong_dan_ngoai = models.URLField(blank=True, null=True)  
    gia_mac_dinh = models.DecimalField(max_digits=6, decimal_places=2)  
    anh_dai_dien = models.ImageField(upload_to="anh_san_pham/", blank=True, null=True)  
    yeu_thich = models.IntegerField(default=0)  
    ngay_tao = models.DateTimeField(auto_now_add=True)  
    ngay_cap_nhat = models.DateTimeField(auto_now=True)  

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
