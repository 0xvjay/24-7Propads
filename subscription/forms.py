from django import forms

from .models import SubscriptionPlan


class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if (
            SubscriptionPlan.objects.filter(name__iexact=name)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Name already exists")
        return name
