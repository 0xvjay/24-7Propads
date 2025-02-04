from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import User


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ("date_joined",)


class EditUserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ("date_joined",)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
