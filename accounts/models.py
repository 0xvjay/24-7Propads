from django.contrib.auth.models import AbstractUser
from django.db import models


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
