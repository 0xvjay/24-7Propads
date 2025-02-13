from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import User
from .utils import is_valid_phone


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ("date_joined", "stripe_id", "checkout_session_id")

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not is_valid_phone(phone):
            raise forms.ValidationError("Invalid phone number")

        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone number already exists")

        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already exists")

        return email


class EditUserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ("date_joined", "stripe_id", "checkout_session_id")

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not is_valid_phone(phone):
            forms.ValidationError("Invalid phone number")

        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Phone number already exists")

        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            User.objects.filter(email__iexact=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Email already exists")

        return email


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if (
            Group.objects.filter(name__iexact=name)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Name already exists")
        return name


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
