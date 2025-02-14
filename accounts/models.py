from django.contrib.auth.models import AbstractUser
from django.db import models

FREE_PLAN_MAX_ADS = 2
FREE_PLAN_MAX_LISTINGS = 3


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=30)
    company = models.CharField(max_length=255)
    address = models.TextField()
    profile = models.ImageField(upload_to="profiles/", default="images/no-image.png")
    is_verified = models.BooleanField(default=False)

    # links
    skype = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()
    linkedin = models.URLField()
    instagram = models.URLField()
    pinterest = models.URLField()

    # stripe
    stripe_id = models.CharField(max_length=255)
    checkout_session_id = models.CharField(max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_role(self):
        if self.is_superuser:
            return "Admin"
        return "User"

    def _can_add_item(self, related_name, free_plan_limit, plan_limit_field):
        """
        Generic helper function to check if a user can add an item
        (advertisement or property).

        Args:
            related_name (str): Name of the related field (e.g., 'advertisements', 'properties').
            free_plan_limit (int): Maximum items allowed on the free plan.
            plan_limit_field (str): Field name for the limit on the subscription plan (e.g., 'max_ads', 'max_listings').

        Returns:
            tuple: (bool is_allowed, str message)
        """

        if self.is_superuser:
            return True

        item_count = getattr(self, related_name).count()

        if item_count >= free_plan_limit:
            return (
                False,
                f"You have reached the maximum number of {related_name} allowed for the free plan.",
            )

        subscription = getattr(self, "subscription", None)
        if subscription and getattr(subscription, "plan", None):
            max_items = getattr(subscription.plan, plan_limit_field)
            if item_count >= max_items:
                return (
                    False,
                    f"You have reached the maximum number of {related_name} allowed for your plan.",
                )

        return True, ""

    def can_add_advertisement(self):
        """
        Determines if the user can add another advertisement.
        """
        return self._can_add_item("advertisements", FREE_PLAN_MAX_ADS, "max_ads")

    def can_add_property(self):
        """
        Check if the user can add another property.
        """
        return self._can_add_item("properties", FREE_PLAN_MAX_LISTINGS, "max_listings")
