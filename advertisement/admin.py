from django.contrib import admin
from django.utils.html import format_html

from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("id", "image_tag", "position", "is_active", "created_at")

    def image_tag(self, obj):
        return format_html('<img src="{}" width=150 />'.format(obj.image.url))

    image_tag.short_description = "Image"
