from django.contrib import admin
from .models import AccessKey

@admin.register(AccessKey)
class AccessKeyAdmin(admin.ModelAdmin):
    list_display = ("masked_key", "is_active", "quota_limit", "quota_exhausted_on", "created_at")
    list_filter = ("is_active",)
