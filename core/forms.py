from django import forms

from .models import (
    FAQ,
    SiteSettings,
    ContactInfo,
    AboutUs,
    TermsAndCondition,
    PrivacyPolicy,
)


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = "__all__"


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = "__all__"


class SiteBasicForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            "title",
            "keywords",
            "description",
            "logo",
            "admin_logo",
            "favicon",
        )


class SiteFooterForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ("footer_description",)


class SiteLinksForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            "facebook",
            "twitter",
            "linkedin",
            "instagram",
            "pinterest",
        )


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = "__all__"


class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = "__all__"


class TermsAndConditionForm(forms.ModelForm):
    class Meta:
        model = TermsAndCondition
        fields = "__all__"


class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"
