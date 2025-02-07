from django.db import models

from accounts.models import User
from property.models import Property


class BrowsingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="browsing_stats"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "-timestamp"]),
        ]
        verbose_name_plural = "Browsing History"


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    query = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    price_min = models.PositiveIntegerField(blank=True, null=True)
    price_max = models.PositiveIntegerField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    post_type = models.CharField(max_length=100, blank=True, null=True)
    area_min = models.PositiveIntegerField(blank=True, null=True)
    area_max = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "-timestamp"]),
            models.Index(fields=["location"]),
            models.Index(fields=["type"]),
            models.Index(fields=["post_type"]),
            models.Index(fields=["price_min", "price_max"]),
            models.Index(fields=["area_min", "area_max"]),
        ]
        verbose_name_plural = "Search History"


class LikeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "property")
        verbose_name_plural = "Like History"
