import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

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


class CustomerSubscriptonListView(LoginRequiredMixin, ListView):
    model = SubscriptionPlan
    template_name = "customer/pages/subscription_plan.html"


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


class CheckoutSessionCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": "34",
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=settings.SITE_URL + "/success.html",
                cancel_url=settings.SITE_URL + "/cancel.html",
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})
