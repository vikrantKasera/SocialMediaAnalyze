from pathlib import Path
from django.db import models


class SeenChannel(models.Model):
    channel_id = models.CharField(max_length=100, unique=True)
    first_seen_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.channel_id


class Creator(models.Model):
    channel_id = models.CharField(max_length=100, unique=True)
    channel_name = models.CharField(max_length=255)
    channel_url = models.URLField(max_length=500)
    custom_url = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    subscribers = models.PositiveBigIntegerField(null=True, blank=True)
    average_recent_views = models.PositiveBigIntegerField(default=0)
    days_since_oldest_video = models.PositiveIntegerField(default=0)
    engagement_flags = models.JSONField(default=list, blank=True)
    recent_videos = models.JSONField(default=list, blank=True)
    search_keywords = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.channel_name


class ResultFile(models.Model):
    file = models.FileField(upload_to="results/")
    filename = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file and not self.filename:
            self.filename = Path(self.file.name).name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.filename
