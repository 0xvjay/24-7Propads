from django import forms

from .models import SubscriptionPlan


class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ("name", "price", "max_listings", "max_ads", "description")

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if (
            SubscriptionPlan.objects.filter(name__iexact=name)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Name already exists")
        return name
