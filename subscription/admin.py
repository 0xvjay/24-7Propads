from django.contrib import admin

from .models import SubscriptionPlan, UserSubscription


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "plan",
        "status",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__email", "plan")


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "duration_days",
        "max_listings",
        "max_ads",
    )
    search_fields = ("name",)
