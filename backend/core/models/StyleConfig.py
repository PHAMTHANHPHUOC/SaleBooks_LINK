from django.db import models

class StyleConfig(models.Model):
    tag = models.CharField(max_length=50, blank=True, unique=True)
    font_family = models.CharField(max_length=200, blank=True, null=True, help_text="Font family CSS")
    font_size = models.CharField(max_length=20, blank=True, null=True, help_text="Font size (px, em, rem)")
    color = models.CharField(max_length=20, blank=True, null=True, help_text="Màu chữ (hex)")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tag} style"

class SiteConfig(models.Model):
    background = models.CharField(max_length=20, blank=True, null=True, help_text="Màu nền chung (hex)")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SiteConfig: background={self.background}"