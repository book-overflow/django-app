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
        fields = ['isbn', 'name', 'edition']
    
    CourseFormSet = inlineformset_factory(Textbook, Course, form=CourseCreationForm, extra=0)
    AuthorFormSet = inlineformset_factory(Textbook, Author, form=AuthorCreationForm, extra=0)
    
    def __init__(self, *args, **kwargs):
        super(TextbookCreationForm, self).__init__(*args, **kwargs)
        self.course_formset = self.CourseFormSet(*args, **kwargs)
        self.author_formset = self.AuthorFormSet(*args, **kwargs)


class TextbookCopyCreationForm2(ModelForm):
    textbook = TextbookCreationForm()
    
    class Meta:
        model = TextbookCopy
        fields = ['condition', 'for_rent', 'for_sale', 'sale_price', 'rent_price', 'image']
