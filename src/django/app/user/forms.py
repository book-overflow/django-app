from .models import Student
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']
