from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith(".edu"):
            raise forms.ValidationError("Email must end with .edu")
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]


class UserProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "date_of_birth",
            "phone_number",
            "street",
            "city",
            "state",
            "zip",
            "image",
        ]
