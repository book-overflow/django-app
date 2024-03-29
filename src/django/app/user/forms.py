from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['date_of_birth', 'phone_number', 'street', 'city', 'state', 'zip', 'image']
