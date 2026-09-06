from django.db import models

class PostingCriteria(models.Model):
    min_subscribers = models.PositiveIntegerField(default=0)
    max_subscribers = models.PositiveIntegerField(default=1000000)
    min_views = models.PositiveIntegerField(default=0)
    max_days_since_posting = models.PositiveIntegerField(default=30)
    additional_criteria = models.TextField(blank=True)
    result_per_keyword = models.PositiveIntegerField(default=10)
    per_page_keyword = models.PositiveIntegerField(default=1)
    video_to_check = models.PositiveIntegerField(default=1)
    recent_days = models.PositiveIntegerField(default=1)
    shorts_max_second = models.PositiveIntegerField(default=1)
    max_creators = models.PositiveIntegerField(default=1000)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Posting Criteria #{self.pk}"
