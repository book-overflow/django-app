from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError
from shared.models import Textbook, Author, Course
from student_profile.decorators import profile_required
from .forms import CourseFormSet, AuthorFormSet, CourseForm, AuthorForm, TextbookForm, TextbookCopyForm

@login_required
@profile_required
def createPost(request):
    if request.method == 'POST':
        course_formset = CourseFormSet(request.POST, prefix='course')
        author_formset = AuthorFormSet(request.POST, prefix='author')
        # course_form = CourseForm(request.POST)
        # author_form = AuthorForm(request.POST)
        textbook_form = TextbookForm(request.POST)
        textbook_copy_form = TextbookCopyForm(request.POST, request.FILES)

        print("request.POST:", request.POST, flush=True)

        try:
            with transaction.atomic():
                if textbook_form.is_valid():
                    textbook = textbook_form.save()
                elif request.POST['isbn']:
                    textbook = Textbook.objects.get(isbn=request.POST['isbn'])
                else:
                    raise ValidationError(textbook_form.errors)
                
                if course_formset.is_valid():
                    print("course_formset is valid...", flush=True)
                    for course_form in course_formset:
                        print(course_form.prefix, flush=True)
                        if course_form.is_valid():
                            print("course_form is valid...", flush=True)
                            course = course_form.save(commit=False)
                            course._university = request.user.student._university
                            course.save()
                            textbook._belongs.add(course)
                        elif request.POST['course_number' + course_form.prefix]:
                            print("course_form is invalid but course_number exists...", flush=True)
                            course = Course.objects.get(course_number=request.POST['course_number' + course_form.prefix])
                        else:
                            print("course_form is invalid...", flush=True)
                            raise ValidationError(course_form.errors)
                else:
                    print("course_formset is invalid...", flush=True)
                    raise ValidationError(course_formset.errors)
                
                if author_formset.is_valid():
                    print('author_formset is valid...', flush=True)
                    for author_form in author_formset:
                        print(author_form.prefix, flush=True)
                        if author_form.is_valid():
                            print("author_form is valid...", flush=True)
                            author = author_form.save()
                            textbook._authors.add(author)
                        elif request.POST['first_name' + author_form.prefix] and request.POST['last_name' + author_form.prefix]:
                            print("author_form is invalid, but first_name and last_name exists...")
                            author = Author.objects.get(first_name=request.POST['first_name' + author_form.prefix], last_name=request.POST['last_name' + author_form.prefix])
                        else:
                            print("author_form is invalid...", flush=True)
                            raise ValidationError(author_form.errors)
                else:
                    print('author_formset is invalid...', flush=True)
                    raise ValidationError(author_formset.errors)

                # if course_form.is_valid():
                #     course = course_form.save(commit=False)
                #     course._university = request.user.student._university
                #     course.save()
                # elif request.POST['course_number']:
                #     course = Course.objects.get(course_number=request.POST['course_number'])
                # else:
                #     raise ValidationError(course_form.errors)
                
                # if author_form.is_valid():
                #     author = author_form.save()
                # elif request.POST['first_name'] and request.POST['last_name']:
                #     author = Author.objects.get(first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                # else:
                #     raise ValidationError(author_form.errors)
                
                # if textbook_form.is_valid():
                #     textbook = textbook_form.save()
                #     textbook._authors.add(author)
                #     textbook._belongs.add(course)
                # elif request.POST['isbn']:
                #     textbook = Textbook.objects.get(isbn=request.POST['isbn'])
                # else:
                #     raise ValidationError(textbook_form.errors)
                
                if textbook_copy_form.is_valid():
                    textbook_copy = textbook_copy_form.save(commit=False)
                    textbook_copy._textbook = textbook
                    textbook_copy._seller = request.user.student
                    textbook_copy.save()
                else:
                    raise ValidationError(textbook_copy_form.errors)
        except ValidationError as e:
            form_errors = e.message_dict
            print("Form errors:", form_errors)

        return redirect('my-textbooks')

    else:
        course_formset = CourseFormSet(prefix='course')
        author_formset = AuthorFormSet(prefix='author')
        # course_form = CourseForm()
        # author_form = AuthorForm()
        textbook_form = TextbookForm()
        textbook_copy_form = TextbookCopyForm()

    return render(request, 'createPost.html', {
        'author_formset': author_formset,
        'course_formset': course_formset,
        # 'course_form': course_form,
        # 'author_form': author_form,
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
