from django.shortcuts import render, redirect
from student_profile.decorators import profile_required
from django.contrib.auth.decorators import login_required
from .forms import CourseCreationForm, AuthorCreationForm, TextbookCreationForm, TextbookCopyCreationForm, TextbookCopyCreationForm2
from shared.models import Textbook, TextbookCopy, Author, Course

@login_required
@profile_required
def createPost(request):
    if request.method == 'POST':
        form = TextbookCopyCreationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            _isbn = data['isbn']
            textbookCopy = form.save(commit=False)
            textbookCopy._seller = request.user.student
            # If ISBN exists in DB
            try:
                textbookCopy._textbook = Textbook.objects.get(isbn = _isbn)
                textbookCopy.save()
            except Textbook.DoesNotExist:
                # If info is available via API
                # ...

                # Else:
                # Check authors
                authors = data['authors'].split(",")
                author_list = []
                for author in authors:
                    author_name = author.lstrip().upper().split(" ")
                    if (len(author_name) == 1):
                        _first_name = author.lstrip().split(" ")[0]
                        _last_name = ""
                    else:
                        _first_name = author.lstrip().split(" ")[0]
                        _last_name = " ".join(author.lstrip().split(" ")[1:])
                    try:
                        author_list.append(Author.objects.get(first_name = _first_name, last_name = _last_name))
                    except Author.DoesNotExist:
                        newAuthor = Author(first_name = _first_name, last_name = _last_name)
                        newAuthor.save()
                        author_list.append(newAuthor)
                # Check course number
                _course_number = data['course'].upper().strip()
                try:
                    course = Course.objects.get(course_number = _course_number)
                except Course.DoesNotExist:
                    newCourse = Course(course_number = _course_number, _university = request.user.student._university, name="", description="")
                    newCourse.save()
                    course = newCourse
                # Create new textbook
                newTextbook = Textbook.objects.create(isbn = _isbn, name = data['name'], edition = data['edition'])
                newTextbook.save()
                newTextbook._authors.set(author_list)
                newTextbook._belongs.set([course])
                newTextbook.save()
                # Create textbook copy
                textbookCopy._textbook = newTextbook
                textbookCopy.save()
                return redirect('my-textbooks')
        else:
            print("Form Error", flush=True)
    else:
        form = TextbookCopyCreationForm()
    context = {'form': form}
    return render(request, 'createPost.html', context)


def createPost2(request):
    if request.method == 'POST':
        print("In the POST request block...", flush=True)
        course_form = CourseCreationForm(request.POST)
        author_form = AuthorCreationForm(request.POST)
        textbook_form = TextbookCreationForm(request.POST)
        textbook_copy_form = TextbookCopyCreationForm2(request.POST, request.FILES)

        print("request.POST:", request.POST, flush=True)
        print("request.FILES:", request.FILES, flush=True)

        if course_form.is_valid() and author_form.is_valid() and textbook_form.is_valid() and textbook_copy_form.is_valid():
            print("All forms are valid...", flush=True)
            # Create course if it doesn't exist
            course_number = course_form.cleaned_data['course_number']
            course, _ = Course.objects.get_or_create(
                course_number=course_number,
                defaults={
                    'name': course_form.cleaned_data['name'],
                    'description': course_form.cleaned_data['description']
                }
            )
            # Create author if it doesn't exist
            author_first_name = author_form.cleaned_data['first_name']
            author_last_name = author_form.cleaned_data['last_name']
            author, _ = Author.objects.get_or_create(
                first_name=author_first_name,
                last_name=author_last_name
            )
            # Create textbook if it doesn't exist
            isbn = textbook_form.cleaned_data['isbn']
            textbook, _ = Textbook.objects.get_or_create(
                isbn=isbn,
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
            textbook_copy._seller = request.user
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
        course_form = CourseCreationForm()
        author_form = AuthorCreationForm()
        textbook_form = TextbookCreationForm()
        textbook_copy_form = TextbookCopyCreationForm2()

    return render(request, 'createPost2.html', {
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
