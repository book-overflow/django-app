from .models import CustomUser
from django.shortcuts import redirect

# Will be used to redirect a logged in user (i.e. if they try to access login/register view)
def guest_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect('browse')
        return view_func(request, *args, **kwargs)
    return wrapper

def profile_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            profile_fields = ['date_of_birth', 'phone_number', 'street', 'city', 'state', 'zip']
            profile = CustomUser.objects.filter(pk=user.pk).values(*profile_fields).first()
            if any(value is None or value == '' for value in profile.values()):
                return redirect('user-register-profile')
        return view_func(request, *args, **kwargs)
    return wrapper
