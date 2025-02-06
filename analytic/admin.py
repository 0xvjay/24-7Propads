from django.contrib import admin

from .models import BrowsingHistory, LikeHistory, SearchHistory


@admin.register(BrowsingHistory)
class BrowsingHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "property", "timestamp")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, *args, **kwargs):
        return False


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, *args, **kwargs):
        return False


@admin.register(LikeHistory)
class LikeHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "property", "timestamp")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, *args, **kwargs):
        return False
