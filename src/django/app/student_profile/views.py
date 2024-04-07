from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileCreationForm, ProfileUpdateForm

@login_required
def createProfile(request):
    if request.method == 'POST':
        form = ProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.student = request.user.student
            profile.save()
            return redirect('browse')
    else:
        form = ProfileCreationForm()
    context = {'form': form}
    return render(request, 'registerProfile.html', context)

@login_required
def getProfile(request):
    return render(request, 'profile.html')

@login_required
def updateProfile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.student.profile)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    else:
        form = ProfileUpdateForm(instance=request.user.student.profile)
    context = {'form': form}
    return render(request, 'updateProfile.html', context)
