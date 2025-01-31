from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "property", "score", "status", "created_at")
    search_fields = ("user", "property", "title")
