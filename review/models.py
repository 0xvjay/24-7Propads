from django.db import models

from accounts.models import User
from property.models import Property


class Review(models.Model):
    class StatusChoices(models.TextChoices):
        FOR_MODERATION = "Requires moderation"
        APPROVED = "Approved"
        REJECTED = "Rejected"

    property = models.ForeignKey(
        Property, related_name="reviews", on_delete=models.CASCADE
    )
    SCORE_CHOICES = tuple([(x, x) for x in range(0, 6)])
    score = models.SmallIntegerField(choices=SCORE_CHOICES)

    title = models.CharField(max_length=255)
    body = models.TextField()

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.FOR_MODERATION,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.property.update_rating()
