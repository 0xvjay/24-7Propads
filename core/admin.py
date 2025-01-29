from django.contrib import admin
from django.utils.html import format_html

from .models import (
    FAQ,
    AboutUs,
    ContactInfo,
    ContactUs,
    PrivacyPolicy,
    SiteSettings,
    TermsAndCondition,
)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active")
    search_fields = ("title",)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("id", "get_description")

    def get_description(self, obj):
        return format_html(obj.description)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TermsAndCondition)
class TermsAndConditionAdmin(admin.ModelAdmin):
    list_display = ("id", "get_description")

    def get_description(self, obj):
        return format_html(obj.description)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "get_description")

    def get_description(self, obj):
        return format_html(obj.description)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
