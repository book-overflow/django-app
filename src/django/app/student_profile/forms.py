from django.forms import ModelForm
from .models import Profile

class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'phone_number', 'street', 'city', 'state', 'zip', 'image']

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'phone_number', 'street', 'city', 'state', 'zip', 'image']
