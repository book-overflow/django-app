from .forms import CustomUserCreationForm, UserProfileForm
from .decorators import guest_required, profile_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@guest_required
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['name'] = form.data["first_name"]
            return redirect('user-login')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required
@profile_required
def profile(request):
    return render(request, 'profile.html')

def setProfile(request):
    return render(request, 'setProfile.html')

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
