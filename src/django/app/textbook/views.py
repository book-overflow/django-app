from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError
from shared.models import Textbook, Author, Course
from student_profile.decorators import profile_required
from .forms import CourseFormSet, AuthorFormSet, TextbookForm, TextbookCopyForm

@login_required
@profile_required
def createPost(request):
    if request.method == 'POST':
        course_formset = CourseFormSet(request.POST, prefix='course')
        author_formset = AuthorFormSet(request.POST, prefix='author')
        textbook_form = TextbookForm(request.POST)
        textbook_copy_form = TextbookCopyForm(request.POST, request.FILES)

        try:
            with transaction.atomic():
                # textbook
                if textbook_form.is_valid():
                    textbook = textbook_form.save()
                elif request.POST['isbn']:
                    textbook = Textbook.objects.get(isbn=request.POST['isbn'])
                else:
                    raise ValidationError(textbook_form.errors)
                
                # courses
                for course_form in course_formset:
                    if course_form.is_valid():
                        course = course_form.save(commit=False)
                        course._university = request.user.student._university
                        course.save()
                        textbook._belongs.add(course)
                    elif request.POST[f'{course_form.prefix}-course_number']:
                        course = Course.objects.get(course_number=request.POST[f'{course_form.prefix}-course_number'])
                        textbook._belongs.add(course)
                    else:
                        raise ValidationError(course_form.errors)
                
                # authors
                for author_form in author_formset:
                    if author_form.is_valid():
                        author = author_form.save()
                        textbook._authors.add(author)
                    elif request.POST[f'{author_form.prefix}-first_name'] and request.POST[f'{author_form.prefix}-last_name']:
                        author = Author.objects.get(first_name=request.POST[f'{author_form.prefix}-first_name'], last_name=request.POST[f'{author_form.prefix}-last_name'])
                        textbook._authors.add(author)
                    else:
                        raise ValidationError(author_form.errors)
                
                # textbook_copy
                if textbook_copy_form.is_valid():
                    textbook_copy = textbook_copy_form.save(commit=False)
                    textbook_copy._textbook = textbook
                    textbook_copy._seller = request.user.student
                    textbook_copy.save()
                else:
                    raise ValidationError(textbook_copy_form.errors)
                
                return redirect('my-textbooks')
        except ValidationError as e:
            form_errors = e.message_dict
            print("Form errors:", form_errors)

    else:
        course_formset = CourseFormSet(prefix='course')
        author_formset = AuthorFormSet(prefix='author')
        textbook_form = TextbookForm()
        textbook_copy_form = TextbookCopyForm()

    return render(request, 'createPost.html', {
        'author_formset': author_formset,
        'course_formset': course_formset,
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
