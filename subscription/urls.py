from django.urls import path

from .views import (
    CheckoutCancelView,
    CheckoutSessionCreateView,
    CheckoutSuccessView,
    CustomerSubscriptonListView,
    StripeConfigView,
    SubscriptionPlanCreateView,
    SubscriptionPlanDeleteView,
    SubscriptionPlanListView,
    SubscriptionPlanUpdateView,
    UserSubscriptionListView,
    stripe_webhook,
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
    path(r"subscriptions/config/", StripeConfigView.as_view(), name="stripe_config"),
    path(r"subscriptions/success/", CheckoutSuccessView.as_view(), name="success"),
    path(r"subscriptions/cancel/", CheckoutCancelView.as_view(), name="cancel"),
    path(r"subscriptions/stripe_webhook/", stripe_webhook),
]
