from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

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

def profile(request):
    return render(request, 'profile.html')

def setProfile(request):
    return render(request, 'setProfile.html')