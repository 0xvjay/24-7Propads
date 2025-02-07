from django import forms
from django.utils import timezone

from accounts.utils import is_valid_phone

from .constant import cities
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
        if PropertyType.objects.filter(name=name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Name already exists")

        return name


class AdminPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        agriculture_formset = self.data.get("agriculture_details-TOTAL_FORMS", 0)
        flat_formset = self.data.get("flat_details-TOTAL_FORMS", 0)
        villa_formset = self.data.get("villa_details-TOTAL_FORMS", 0)
        house_formset = self.data.get("house_details-TOTAL_FORMS", 0)
        office_formset = self.data.get("office_details-TOTAL_FORMS", 0)
        plot_formset = self.data.get("plot_details-TOTAL_FORMS", 0)

        count = 0
        if int(agriculture_formset) > 0:
            count += 1
        if int(flat_formset) > 0:
            count += 1
        if int(villa_formset) > 0:
            count += 1
        if int(house_formset) > 0:
            count += 1
        if int(office_formset) > 0:
            count += 1
        if int(plot_formset) > 0:
            count += 1

        if count > 1:
            self.add_error(
                None,
                "You can only have one type of property detail (Agriculture, Flat, Villa, etc.) associated with a Property.",
            )
        return cleaned_data


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class PropertyForm(forms.ModelForm):
    images = MultipleFileField()
    state = forms.ChoiceField(choices=[(state, state) for state, _ in cities])
    city = forms.ChoiceField(choices=[])

    class Meta:
        model = Property
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "0-state" in self.data:
            state_selected = self.data.get("0-state")
            self.fields["city"].choices = [
                (city, city)
                for st, city_list in cities
                if st == state_selected
                for city in city_list[0]
            ]
        else:
            self.fields["city"].choices = []

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not is_valid_phone(phone):
            raise forms.ValidationError("Invalid phone number")
        return phone


class AgricultureLandForm(forms.ModelForm):
    class Meta:
        model = AgricultureLand
        exclude = ("property",)


class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        exclude = ("property",)

    def available_from(self):
        available_from = self.cleaned_data.get("available_from")
        if available_from <= timezone.now().date():
            raise forms.ValidationError("The date must be in the future.")
        return available_from


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        exclude = ("property",)

    def available_from(self):
        available_from = self.cleaned_data.get("available_from")
        if available_from <= timezone.now().date():
            raise forms.ValidationError("The date must be in the future.")
        return available_from


class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        exclude = ("property",)

    def available_from(self):
        available_from = self.cleaned_data.get("available_from")
        if available_from <= timezone.now().date():
            raise forms.ValidationError("The date must be in the future.")
        return available_from


class VillaForm(forms.ModelForm):
    class Meta:
        model = Villa
        exclude = ("property",)

    def available_from(self):
        available_from = self.cleaned_data.get("available_from")
        if available_from <= timezone.now().date():
            raise forms.ValidationError("The date must be in the future.")
        return available_from


class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        exclude = ("property",)
