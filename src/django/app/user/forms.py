from shared.models import Student
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']
