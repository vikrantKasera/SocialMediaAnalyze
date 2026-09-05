from django.contrib import admin
from .models import PostingCriteria

@admin.register(PostingCriteria)
class PostingCriteriaAdmin(admin.ModelAdmin):
    list_display = ("id", "min_subscribers", "max_subscribers", "min_views", "max_days_since_posting", "is_active")
