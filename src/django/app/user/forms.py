from shared.models import Student
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith(".edu"):
            raise forms.ValidationError("Email must end with .edu")
        return email
