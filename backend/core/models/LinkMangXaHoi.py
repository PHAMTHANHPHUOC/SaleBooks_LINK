from django.db import models
from django.http import JsonResponse

class LinkProfile(models.Model):
    name = models.CharField(max_length=100, default="My Links")
    links = models.TextField() 
   

    class Meta:
        verbose_name = "Link Profile"
        verbose_name_plural = "Link Profiles"

    def __str__(self):
        return self.name
    def get_formatted_links(self):
        """Trả về links với format {url: name}"""
        if self.links and isinstance(self.links, dict):
            return {url: name for name, url in self.links.items()}
        return {}