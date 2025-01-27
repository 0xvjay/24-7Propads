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
        exclude = ("views",)

    def is_valid(self):
        print(self.data)
        print(self.errors)
        return super().is_valid()


class AgricultureLandForm(forms.ModelForm):
    class Meta:
        model = AgricultureLand
        fields = "__all__"


class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = "__all__"


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = "__all__"


class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = "__all__"


class VillaForm(forms.ModelForm):
    class Meta:
        model = Villa
        fields = "__all__"


class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        fields = "__all__"
