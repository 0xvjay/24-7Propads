import json
import logging
from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http.response import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView

from accounts.models import User
from core.views import (
    BaseAdminCreateView,
    BaseAdminDeleteView,
    BaseAdminListView,
    BaseAdminUpdateView,
)

from .forms import SubscriptionPlanForm
from .models import SubscriptionPlan, UserSubscription
from .utils import StripeSubscriptionHandler

logger = logging.getLogger("app")


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


class StripeConfigView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"publicKey": settings.STRIPE_PUBLISHABLE_KEY}, safe=False)


class CheckoutSessionCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        stripe_handler = StripeSubscriptionHandler(settings.STRIPE_SECRET_KEY)

        try:
            plan_id = json.loads(request.body).get("plan_id")
            if not plan_id:
                return JsonResponse({"error": "Bad Request"})

            try:
                price_id = SubscriptionPlan.objects.get(id=plan_id).stripe_price_id
            except SubscriptionPlan.DoesNotExist:
                return JsonResponse({"error": "Invalid Plan ID"})

            session_id = stripe_handler.create_checkout_session(
                price_id, self.request.user
            )
            if not session_id:
                return JsonResponse({"error": "Server Error"})

            user = self.request.user
            user.checkout_session_id = session_id
            user.save()

            return JsonResponse({"sessionId": session_id})
        except Exception as e:
            return JsonResponse({"error": str(e)})


class CheckoutSuccessView(TemplateView):
    template_name = "customer/pages/checkout/success.html"


class CheckoutCancelView(TemplateView):
    template_name = "customer/pages/checkout/cancel.html"


@csrf_exempt
def stripe_webhook(request):
    stripe_handler = StripeSubscriptionHandler(settings.STRIPE_SECRET_KEY)

    try:
        event = stripe_handler.create_event(request.body)
    except Exception:
        return HttpResponse(status=400)

    if not event:
        return HttpResponse(status=400)

    event_handlers = {
        "checkout.session.completed": handle_checkout_session_completed,
        "invoice.paid": handle_invoice_paid,
        "customer.subscription.updated": handle_subscription_updated,
        "customer.subscription.deleted": handle_subscription_deleted,
    }

    handler = event_handlers.get(event.type)
    if handler:
        handler(event, stripe_handler)

    return HttpResponse(status=200)


def handle_checkout_session_completed(event, stripe_handler: StripeSubscriptionHandler):
    """Handles the checkout.session.completed event."""

    stripe_id = event.data.object.get("customer")
    checkout_session_id = event.data.object.get("id")
    subscription_id = event.data.object.get("subscription")

    user = User.objects.filter(checkout_session_id=checkout_session_id).first()
    if user:
        user.stripe_id = stripe_id
        user.save()

        subscription = stripe_handler.retrieve_subscription_plan(subscription_id)
        product_id = subscription["plan"]["product"]
        plan = SubscriptionPlan.objects.get(stripe_product_id=product_id)

        start_date = datetime.fromtimestamp(
            subscription.current_period_start, tz=timezone.utc
        ).date()
        end_date = datetime.fromtimestamp(
            subscription.current_period_end, tz=timezone.utc
        ).date()

        with transaction.atomic():
            UserSubscription.objects.create(
                user=user, plan=plan, start_date=start_date, end_date=end_date
            )


def handle_invoice_paid(event, stripe_handler: StripeSubscriptionHandler):
    """Handles the invoice.paid event."""

    subscription_id = event.data.object.get("subscription")
    subscription = stripe_handler.retrieve_subscription_plan(subscription_id)

    user_subscription = UserSubscription.objects.get(
        user__stripe_id=subscription["customer"]
    )

    user_subscription.end_date = datetime.fromtimestamp(
        subscription.current_period_end, tz=timezone.utc
    ).date()
    user_subscription.save()


def handle_subscription_updated(event, stripe_handler: StripeSubscriptionHandler):
    """Handles the customer.subscription.updated event."""

    subscription_id = event.data.object.get("id")
    subscription = stripe_handler.retrieve_subscription_plan(subscription_id)
    user_subscription = UserSubscription.objects.get(
        user__stripe_id=subscription["customer"]
    )
    user_subscription.end_date = datetime.fromtimestamp(
        subscription.current_period_end, tz=timezone.utc
    ).date()
    user_subscription.save()


def handle_subscription_deleted(event, stripe_handler: StripeSubscriptionHandler):
    """Handles the customer.subscription.deleted event."""

    subscription_id = event.data.object.get("id")
    subscription = stripe_handler.retrieve_subscription_plan(subscription_id)

    user_subscription = UserSubscription.objects.get(
        user__stripe_id=subscription["customer"]
    )
    user_subscription.end_date = datetime.fromtimestamp(
        subscription.current_period_end, tz=timezone.utc
    ).date()
    user_subscription.status = "Canceled"
    user_subscription.save()
