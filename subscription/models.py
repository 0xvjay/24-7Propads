import logging

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils.timezone import now

from accounts.models import User

from .utils import StripeSubscriptionHandler

logger = logging.getLogger(__name__)


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    max_listings = models.PositiveSmallIntegerField()
    max_ads = models.PositiveSmallIntegerField()
    description = models.TextField()

    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    class StatusType(models.TextChoices):
        ACTIVE = "Active"
        EXPIRED = "Expired"
        CANCELED = "Canceled"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.PROTECT, related_name="subscriptions"
    )
    status = models.CharField(
        choices=StatusType.choices, default=StatusType.ACTIVE, max_length=20
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_active(self):
        return (
            self.status == UserSubscription.StatusType.ACTIVE
            and self.start_date <= now().date() <= self.end_date
        )

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.status})"


@receiver(post_save, sender=SubscriptionPlan)
def _post_save_receiver(sender, instance: SubscriptionPlan, created, *args, **kwargs):
    stripe_handler = StripeSubscriptionHandler(settings.STRIPE_SECRET_KEY)
    try:
        if created:
            response = stripe_handler.create_plan(
                name=instance.name,
                description=instance.description,
                price=instance.price,
            )
        else:
            response = stripe_handler.update_plan(
                instance.stripe_product_id,
                instance.stripe_price_id,
                instance.name,
                instance.description,
                instance.price,
            )
        if response:
            SubscriptionPlan.objects.filter(id=instance.id).update(
                stripe_product_id=response[0], stripe_price_id=response[1]
            )
    except Exception as e:
        logger.exception(e)


@receiver(pre_delete, sender=SubscriptionPlan)
def _post_delete_receiver(sender, instance: SubscriptionPlan, *args, **kwargs):
    stripe_handler = StripeSubscriptionHandler(settings.STRIPE_SECRET_KEY)
    try:
        stripe_handler.delete_plan(instance.stripe_product_id, instance.stripe_price_id)
    except Exception as e:
        logger.exception(e)
