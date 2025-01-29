from django.contrib import admin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "show_profile", "email", "phone", "company", "is_verified")
    search_fields = ("email", "phone", "company", "first_name", "last_name")

    def show_profile(self, obj):
        if obj.profile:
            return format_html('<img src="{}" width=150 />'.format(obj.profile.url))

    show_profile.short_description = "Profile"
