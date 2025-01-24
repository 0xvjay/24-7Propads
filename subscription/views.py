from core.views import (
    BaseAdminCreateView,
    BaseAdminDeleteView,
    BaseAdminListView,
    BaseAdminUpdateView,
)

from .forms import SubscriptionPlanForm
from .models import SubscriptionPlan, UserSubscription


class SubscriptionPlanListView(BaseAdminListView):
    model = SubscriptionPlan
    template_name = "admin/pages/subscription_plan/index.html"


class SubscriptionPlanCreateView(BaseAdminCreateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = "admin/pages/subscription_plan/create.html"
    success_url = "/admin/subscription_plans/"


class SubscriptionPlanUpdateView(BaseAdminUpdateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = "admin/pages/subscription_plan/edit.html"
    success_url = "/admin/subscription_plans/"


class SubscriptionPlanDeleteView(BaseAdminDeleteView):
    model = SubscriptionPlan
    template_name = "admin/pages/subscription_plan/index.html"
    success_url = "/admin/subscription_plans/"


class UserSubscriptionListView(BaseAdminListView):
    model = UserSubscription
    template_name = "admin/pages/user_subscription.html"
