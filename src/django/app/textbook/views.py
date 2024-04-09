from django.shortcuts import render
from student_profile.decorators import profile_required
from django.contrib.auth.decorators import login_required

@login_required
@profile_required
def createPost(request):
    return render(request, 'createPost.html')

@login_required
@profile_required
def getPost(request):
    return render(request, 'getPost.html')

@login_required
@profile_required
def getMyTextbooks(request):
    return render(request, 'MyTextbooks.html')
