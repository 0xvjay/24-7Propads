from django import forms

from .models import (
    AgricultureLand,
    Flat,
    House,
    Office,
    Plot,
    Property,
    PropertyType,
    Villa,
)


class TypeForm(forms.ModelForm):
    class Meta:
        model = PropertyType
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError("Name is required")
        if PropertyType.objects.filter(name=name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Name already exists")

        return name


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ("views", "user")


class AgricultureLandForm(forms.ModelForm):
    class Meta:
        model = AgricultureLand
        exclude = ("property",)


class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        exclude = ("property",)


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        exclude = ("property",)


class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        exclude = ("property",)


class VillaForm(forms.ModelForm):
    class Meta:
        model = Villa
        exclude = ("property",)


class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        exclude = ("property",)
