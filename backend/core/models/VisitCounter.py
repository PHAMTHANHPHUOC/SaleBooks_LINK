from django.db import models
from django.utils import timezone

class VisitCounter(models.Model):
    page_name = models.CharField(max_length=100, unique=True, default='homepage')
    total_visits = models.IntegerField(default=0)
    today_visits = models.IntegerField(default=0)
    last_visit_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'visit_counter'
    
    def __str__(self):
        return f"{self.page_name}: {self.total_visits} visits"

class VisitLog(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    page_visited = models.CharField(max_length=100)
    visit_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'visit_logs'