from django.shortcuts import render, redirect
from student_profile.decorators import profile_required
from django.contrib.auth.decorators import login_required
from .forms import TextbookCopyCreationForm
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
                print("Save Complete", flush=True)
                return redirect('my-textbooks')
        else:
            print("Form Error", flush=True)
    else:
        form = TextbookCopyCreationForm()
    context = {'form': form}
    return render(request, 'createPost.html', context)

@login_required
@profile_required
def getPost(request):
    return render(request, 'getPost.html')

@login_required
@profile_required
def getMyTextbooks(request):
    return render(request, 'MyTextbooks.html')
