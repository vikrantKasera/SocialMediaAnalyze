from django.contrib import admin
from .models import Creator, ResultFile, SeenChannel


@admin.register(SeenChannel)
class SeenChannelAdmin(admin.ModelAdmin):
    list_display = ("channel_id", "first_seen_at", "last_seen_at")
    search_fields = ("channel_id",)


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ("channel_name", "country", "subscribers", "average_recent_views", "created_at")
    search_fields = ("channel_name", "channel_id", "custom_url")
    list_filter = ("country",)

@admin.register(ResultFile)
class ResultFileAdmin(admin.ModelAdmin):
    list_display = ("filename", "created_at")
    readonly_fields = ("created_at",)
