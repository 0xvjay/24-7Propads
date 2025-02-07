from django.urls import path

from .views import (
    SubscriptionPlanCreateView,
    SubscriptionPlanDeleteView,
    SubscriptionPlanListView,
    SubscriptionPlanUpdateView,
    UserSubscriptionListView,
    CustomerSubscriptonListView,
    CheckoutSessionCreateView,
    stripe_config,
)

app_name = "subscription"
urlpatterns = [
    path(
        r"admin/subscription_plans/",
        SubscriptionPlanListView.as_view(),
        name="subscription_plans",
    ),
    path(
        r"admin/subscription_plans/add",
        SubscriptionPlanCreateView.as_view(),
        name="add_subscription_plan",
    ),
    path(
        r"admin/subscription_plans/edit/<int:pk>/",
        SubscriptionPlanUpdateView.as_view(),
        name="edit_subscription_plan",
    ),
    path(
        r"admin/subscription_plans/delete/<int:pk>/",
        SubscriptionPlanDeleteView.as_view(),
        name="delete_subscription_plan",
    ),
    path(
        r"admin/user_subscriptions/",
        UserSubscriptionListView.as_view(),
        name="user_subscriptions",
    ),
    path(
        r"subscriptions/",
        CustomerSubscriptonListView.as_view(),
        name="customer_subscription_plans",
    ),
    path(
        r"subscriptions/checkout/", CheckoutSessionCreateView.as_view(), name="checkout"
    ),
    path(r"config/", stripe_config, name="stripe_config"),
]
