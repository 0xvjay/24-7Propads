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

    def __str__(self):
        return "Site Settings"

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

    class Meta:
        verbose_name_plural = "Site Settings"


class ContactInfo(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.name

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

    class Meta:
        verbose_name_plural = "Contact Info"


class AboutUs(BasePage):
    def __str__(self):
        return "About Us"

    def save(self, *args, **kwargs):
        if not self.pk and AboutUs.objects.exists():
            raise ValidationError("Only one instance of this model is allowed.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "About Us"


class TermsAndCondition(BasePage):
    def __str__(self):
        return "Terms and Conditions"

    def save(self, *args, **kwargs):
        if not self.pk and TermsAndCondition.objects.exists():
            raise ValidationError("Only one instance of this model is allowed.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Terms & Condition"


class PrivacyPolicy(BasePage):
    def __str__(self):
        return "Privacy Policy"

    def save(self, *args, **kwargs):
        if not self.pk and PrivacyPolicy.objects.exists():
            raise ValidationError("Only one instance of this model is allowed.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Privacy Policy"


class FAQ(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name_plural = "Contact Us"
