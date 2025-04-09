# models.py
from django.db import models
from django.contrib.postgres.fields import JSONField  # For Django < 3.1
# from django.db.models import JSONField  # For Django ≥ 3.1

class DjangoSearchLog(models.Model):
    query = models.CharField(max_length=255)
    user_id = models.CharField(max_length=36, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    results_count = models.PositiveIntegerField(default=0)
    metadata = JSONField(default=dict)
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['query']),
        ]