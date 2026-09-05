from django.contrib import admin
from .models import ResultFile

@admin.register(ResultFile)
class ResultFileAdmin(admin.ModelAdmin):
    list_display = ("filename", "created_at")
    readonly_fields = ("created_at",)
