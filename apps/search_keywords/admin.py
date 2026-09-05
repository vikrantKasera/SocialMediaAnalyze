from django.contrib import admin
from .models import SearchKeyword

@admin.register(SearchKeyword)
class SearchKeywordAdmin(admin.ModelAdmin):
    list_display = ("keyword", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("keyword",)
