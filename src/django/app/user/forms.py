from shared.models import Student
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(ModelForm):
    class Meta:
        model = Student
        fields = ['date_of_birth', 'phone_number', 'street', 'city', 'state', 'zip', 'image']
