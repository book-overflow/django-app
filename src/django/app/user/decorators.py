from django.shortcuts import redirect

# Specifically used to restrict logged in users from accessing login and register views
def guest_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect('browse')
        return view_func(request, *args, **kwargs)
    return wrapper
