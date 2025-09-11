from django.db import models

class StyleConfig(models.Model):
    tag = models.CharField(max_length=50, blank=True, unique=True)
    font_family = models.CharField(max_length=100, blank=True, null=True)
    font_size = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True, help_text="Màu chữ (hex)")
    background = models.CharField(max_length=20, blank=True, null=True, help_text="Màu nền (hex)")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tag} style"
