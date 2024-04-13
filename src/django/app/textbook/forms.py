from django import forms
from django.forms import ModelForm, inlineformset_factory
from shared.models import Course, Author, Textbook, TextbookCopy

class TextbookCopyCreationForm(ModelForm):
    isbn = forms.IntegerField()
    name = forms.CharField(max_length=255)
    authors = forms.CharField(max_length=255)
    course = forms.CharField(max_length=255)
    edition = forms.IntegerField()
    class Meta:
        model = TextbookCopy
        fields = ['condition', 'for_rent', 'for_sale', 'sale_price', 'rent_price', 'image']

class CourseCreationForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'name', 'description']

class AuthorCreationForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']

class TextbookCreationForm(ModelForm):
    class Meta:
        model = Textbook
        fields = ['isbn', 'title', 'edition']

class TextbookCopyCreationForm2(ModelForm):
    class Meta:
        model = TextbookCopy
        fields = ['condition', 'for_rent', 'for_sale', 'sale_price', 'rent_price', 'image']
