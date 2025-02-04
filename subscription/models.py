from django.db import models
from django.utils.timezone import now

from accounts.models import User


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    duration_days = models.PositiveSmallIntegerField()
    max_listings = models.PositiveSmallIntegerField()
    max_ads = models.PositiveSmallIntegerField()
    description = models.TextField()

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
