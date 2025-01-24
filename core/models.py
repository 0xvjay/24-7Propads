from django.db import models
from django.forms import ValidationError


class BasePage(models.Model):
    description = models.TextField()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        raise ValidationError("You cannot delete this instance.")

    @classmethod
    def load(self):
        """Helper to get the singleton instance."""
        obj, created = self.objects.get_or_create(pk=1)
        return obj


# site settings & pages CMS
class SiteSettings(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="site_settings/", null=True, blank=True)
    admin_logo = models.ImageField(upload_to="site_settings/", null=True, blank=True)
    favicon = models.ImageField(upload_to="site_settings/", null=True, blank=True)

    footer_description = models.TextField(null=True, blank=True)

    # social links
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    pinterest = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("Only one instance of this model is allowed.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("You cannot delete this instance.")

    @classmethod
    def load(self):
        """Helper to get the singleton instance."""
        obj, created = self.objects.get_or_create(pk=1)
        return obj


class ContactInfo(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        if not self.pk and ContactInfo.objects.exists():
            raise ValidationError("Only one instance of this model is allowed.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("You cannot delete this instance.")

    @classmethod
    def load(self):
        """Helper to get the singleton instance."""
        obj, created = self.objects.get_or_create(pk=1)
        return obj


class AboutUs(BasePage):
    def save(self, *args, **kwargs):
        if not self.pk and AboutUs.objects.exists():
            raise ValidationError("Only one instance of this model is allowed.")
        super().save(*args, **kwargs)


class TermsAndCondition(BasePage):
    def save(self, *args, **kwargs):
        if not self.pk and TermsAndCondition.objects.exists():
            raise ValidationError("Only one instance of this model is allowed.")
        super().save(*args, **kwargs)


class PrivacyPolicy(BasePage):
    def save(self, *args, **kwargs):
        if not self.pk and PrivacyPolicy.objects.exists():
            raise ValidationError("Only one instance of this model is allowed.")
        super().save(*args, **kwargs)


class FAQ(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField()
    description = models.TextField(null=True, blank=True)


class ContactUs(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
