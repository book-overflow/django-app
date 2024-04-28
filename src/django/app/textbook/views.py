from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from shared.models import TextbookCopy, Textbook, Author, Course
from student_profile.decorators import profile_required
from .forms import CourseFormSet, AuthorFormSet, TextbookForm, TextbookCopyForm, AuthorForm, CourseForm
from .api import searchISBN
from django.contrib import messages
from django.forms import modelformset_factory
from django.db.models import Q, Count

@login_required
@profile_required
def createListing(request):
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
                messages.info(request, message="New Listing Created",extra_tags="success")
                return redirect('get-user-listings')
        except ValidationError as e:
            form_errors = e.message_dict
            print("Form errors:", form_errors)

    elif request.method == 'GET':
        course_formset = CourseFormSet(prefix='course')
        author_formset = AuthorFormSet(prefix='author')
        textbook_form = TextbookForm()
        textbook_copy_form = TextbookCopyForm()
        if request.GET.get('isbn'):
            isbn = request.GET.get('isbn')
            try:
                textbook = Textbook.objects.get(isbn=int(isbn))
                textbook_initial = {
                    'isbn': textbook.isbn,
                    'title': textbook.title,
                }
                author_initial = [{'first_name': author.first_name, 'last_name': author.last_name} for author in textbook._authors.all()]
            except Exception as e:
                textbook = searchISBN(isbn)
                if textbook: # Only set initial when search result is returned
                    textbook_initial = {
                        'isbn': textbook['isbn'],
                        'title': textbook['title'],
                    }
                    author_initial = [{'first_name': author.split()[0], 'last_name': author.split()[-1]} for author in textbook['authors']]
                else: textbook_initial, author_initial = None, None
            if textbook_initial and author_initial:
                textbook_form = TextbookForm(initial=textbook_initial)
                author_formset = AuthorFormSet(initial=author_initial, prefix='author')[:len(author_initial)] # Do not send extra form when populated with Search

    return render(request, 'createListing.html', {
        'author_formset': author_formset,
        'course_formset': course_formset,
        'textbook_form': textbook_form,
        'textbook_copy_form': textbook_copy_form
    })


@login_required
@profile_required
def getListings(request):
    print("hello", flush=True)
    query = request.GET.get('query')    
    queryset = Textbook.objects.all()

    if not query:
        return render(request, 'listings.html')

    terms = query.split()
    final_filter = Q()
    
    for term in terms:
        # Try to match the term with ISBN
        final_filter |= Q(isbn__icontains=term)
        
        # Try to match the term with title
        final_filter |= Q(title__icontains=term)
        
        # Try to match the term with authors' names
        final_filter |= Q(_authors__first_name__icontains=term) | Q(_authors__last_name__icontains=term)
        
        # Try to match the term with course name or course number
        final_filter |= Q(_belongs__name__icontains=term) | Q(_belongs__course_number__icontains=term)
    
    queryset = queryset.filter(final_filter)
    queryset = queryset.annotate(
        num_matches=Count('isbn') + Count('title') + Count('_authors') + Count('_belongs')
    )
    queryset = queryset.order_by('-num_matches')

    print(queryset.distinct(), flush=True)
    return render(request, 'listings.html', context={'results': queryset}) # Added Temp. context for testing

@login_required
@profile_required
def getListing(request, id):
    try:
        listing = TextbookCopy.objects.get(pk=id)
    except TextbookCopy.DoesNotExist:
        return HttpResponse('<div>Listing not found</div>')
    
    return render(request, 'listing.html', {
        'listing': listing,
        # django templates restricts access to attributes that begin with underscore
        'textbook': listing._textbook,
        'authors': list(listing._textbook._authors.all()),
        'courses': list(listing._textbook._belongs.all()),
        'seller': listing._seller
    })

@login_required
@profile_required
def getUserListings(request):
    listings = TextbookCopy.objects.filter(_seller=request.user.student)

    # django templates restricts access to attributes that begin with underscore
    contexts = []
    for listing in listings:
        contexts.append({
            'listing': listing,
            'textbook': listing._textbook,
            'authors': list(listing._textbook._authors.all()),
            'courses': list(listing._textbook._belongs.all())
        })
    
    return render(request, 'userListings.html', {
        'contexts': contexts
    })

@login_required
@profile_required
def getUserListing(request, id):
    try:
        listing = TextbookCopy.objects.get(pk=id)
        
        if listing._seller != request.user.student:
            return HttpResponse('<div>You do not own this listing.</div>')
    
    except TextbookCopy.DoesNotExist:
        return HttpResponse('<div>Listing not found</div>')
    
    return render(request, 'userListing.html', {
        'listing': listing,
        # django templates restricts access to attributes that begin with underscore
        'textbook': listing._textbook,
        'authors': list(listing._textbook._authors.all()),
        'courses': list(listing._textbook._belongs.all()),
        'condition': listing.condition.replace('_', ' ')
    })


@login_required
@profile_required
def deleteUserListing(request, id):
    try:
        listing = TextbookCopy.objects.get(pk=id)
        listing.delete()
        messages.info(request, message="Listing Deleted",extra_tags="success")
        return redirect('get-user-listings')
    except TextbookCopy.DoesNotExist:
        return HttpResponse('<div>Listing not found</div>')
    
@login_required
@profile_required
def editUserListing(request, id):
    CourseModelFormSet = modelformset_factory(Course, form=CourseForm, extra=0, can_delete=True)
    AuthorModelFormSet = modelformset_factory(Author, form=AuthorForm, extra=0)
    listing = TextbookCopy.objects.get(pk=id)
    textbook = listing._textbook
    authors = textbook._authors.all()
    courses = textbook._belongs.all()

    if request.method == 'POST':
        # Only allow listing & course info update 
        textbook_copy_form = TextbookCopyForm(request.POST or None, request.FILES, instance=listing)
        course_formset = CourseModelFormSet(request.POST or None, prefix='course')
        try:
            textbook._belongs.clear()
            for course_form in course_formset: 
                if f'{course_form.prefix}-DELETE' not in request.POST:
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
            textbook.save()
            if textbook_copy_form.is_valid():
                textbook_copy_form.save()
            else:
                raise ValidationError(textbook_copy_form.errors)
            messages.info(request, message="Listing Updated",extra_tags="success")
            return redirect('get-user-listings')
        except ValidationError as e:
            print(e)
    else:
        textbook_copy_form = TextbookCopyForm(request.FILES, instance=listing)
        textbook_form = TextbookForm(instance=textbook)
        course_formset = CourseModelFormSet(queryset=courses, prefix='course')
        author_formset = AuthorModelFormSet(queryset=authors, prefix='author')
        return render(request, 'createListing.html', {
                'for_edit': True,
                'author_formset': author_formset,
                'course_formset': course_formset,
                'textbook_form': textbook_form,
                'textbook_copy_form': textbook_copy_form
        })