from .forms import CustomUserCreationForm, UserProfileForm
from .decorators import guest_required, profile_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

# Add guest_required decorator to built-in LoginView
class CustomLoginView(LoginView):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return guest_required(view)

# Require users to be logged in/authenticated to access built-in LogoutView
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user-login')
        return super().get(request, *args, **kwargs)

@guest_required
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate the user
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            if user is not None:
                # Log the user in
                login(request, user)
                request.session['name'] = form.cleaned_data["first_name"]
                return redirect('user-register-profile')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required
def registerProfile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    else:
        form = UserProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'registerProfile.html', context)

@login_required
@profile_required
def getProfile(request):
    return render(request, 'profile.html')

@login_required
@profile_required
def updateProfile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    else:
        form = UserProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'updateProfile.html', context)
