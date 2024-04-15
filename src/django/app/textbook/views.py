from django.shortcuts import render, redirect
from student_profile.decorators import profile_required
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, AuthorForm, TextbookForm, TextbookCopyForm
from shared.models import Textbook, Author, Course

@login_required
@profile_required
def createPost(request):
    if request.method == 'POST':
        print("In the POST request block...", flush=True)
        course_form = CourseForm(request.POST)
        author_form = AuthorForm(request.POST)
        textbook_form = TextbookForm(request.POST)
        textbook_copy_form = TextbookCopyForm(request.POST, request.FILES)

        print("request.POST:", request.POST, flush=True)
        print("request.FILES:", request.FILES, flush=True)

        if course_form.is_valid() and author_form.is_valid() and textbook_form.is_valid() and textbook_copy_form.is_valid():
            print("All forms are valid...", flush=True)
            # Create course if it doesn't exist
            course, _ = Course.objects.get_or_create(
                course_number=course_form.cleaned_data['course_number'],
                defaults={
                    'name': course_form.cleaned_data['name'],
                    'description': course_form.cleaned_data['description'],
                    '_university': request.user.student._university
                }
            )
            # Create author if it doesn't exist
            author, _ = Author.objects.get_or_create(
                first_name=author_form.cleaned_data['first_name'],
                last_name=author_form.cleaned_data['last_name']
            )
            # Create textbook if it doesn't exist
            textbook, _ = Textbook.objects.get_or_create(
                isbn=textbook_form.cleaned_data['isbn'],
                defaults={
                    'title': textbook_form.cleaned_data['title'],
                    'edition': textbook_form.cleaned_data['edition']
                }
            )
            # Add author to textbook if it isn't already associated
            textbook._authors.add(author)
            # Add course to textbook if it isn't already associated
            textbook._belongs.add(course)
            # Create textbook copy
            textbook_copy = textbook_copy_form.save(commit=False)
            textbook_copy._textbook = textbook
            textbook_copy._seller = request.user.student
            textbook_copy.save()
            # Redirect to my textbooks page
            return redirect('my-textbooks')
        
        else:
            print("Not all forms are valid...", flush=True)
            print("Course form errors:", course_form.errors, flush=True)
            print("Author form errors:", author_form.errors, flush=True)
            print("Textbook form errors:", textbook_form.errors, flush=True)
            print("Textbook copy form errors:", textbook_copy_form.errors, flush=True)

    else:
        print("In the GET request block...", flush=True)
        # If not a POST request, create empty forms
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
