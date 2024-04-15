from django.shortcuts import render, redirect
from student_profile.decorators import profile_required
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, AuthorForm, TextbookForm, TextbookCopyForm
from shared.models import Textbook, Author, Course

@login_required
@profile_required
def createPost(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        author_form = AuthorForm(request.POST)
        textbook_form = TextbookForm(request.POST)
        textbook_copy_form = TextbookCopyForm(request.POST, request.FILES)

        if course_form.is_valid():
            course = course_form.save(commit=False)
            course._university = request.user.student._university
            course.save()
        elif request.POST['course_number']:
            course = Course.objects.get(course_number=request.POST['course_number'])
        else:
            print("Course form errors:", course_form.errors, flush=True)
        
        if author_form.is_valid():
            author = author_form.save()
        elif request.POST['first_name'] and request.POST['last_name']:
            author = Author.objects.get(first_name=request.POST['first_name'], last_name=request.POST['last_name'])
        else:
            print("Author form errors:", author_form.errors, flush=True)
        
        if textbook_form.is_valid():
            textbook = textbook_form.save()
            textbook._authors.add(author)
            textbook._belongs.add(course)
        elif request.POST['isbn']:
            textbook = Textbook.objects.get(isbn=request.POST['isbn'])
        else:
            print("Textbook form errors:", textbook_form.errors, flush=True)
        
        if textbook_copy_form.is_valid():
            textbook_copy = textbook_copy_form.save(commit=False)
            textbook_copy._textbook = textbook
            textbook_copy._seller = request.user.student
            textbook_copy.save()
        else:
            print("Textbook copy form errors:", textbook_copy_form.errors, flush=True)

        return redirect('my-textbooks')

    else:
        course_form = CourseForm()
        author_form = AuthorForm()
        textbook_form = TextbookForm()
        textbook_copy_form = TextbookCopyForm()

    return render(request, 'createPost.html', {
        'course_form': course_form,
        'author_form': author_form,
        'textbook_form': textbook_form,
        'textbook_copy_form': textbook_copy_form
    })

@login_required
@profile_required
def getPost(request):
    return render(request, 'getPost.html')

@login_required
@profile_required
def getMyTextbooks(request):
    return render(request, 'MyTextbooks.html')
