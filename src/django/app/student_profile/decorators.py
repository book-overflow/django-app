from django.shortcuts import redirect

def profile_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if hasattr(user.student, 'profile'):
                return view_func(request, *args, **kwargs)
            else:
                return redirect('create-profile')
    return wrapper

# Specifically used to restrict students with profile from accessing createProfile view
def no_profile_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if hasattr(user.student, 'profile'):
                return redirect('get-profile')
            else:
                return view_func(request, *args, **kwargs)
    return wrapper
