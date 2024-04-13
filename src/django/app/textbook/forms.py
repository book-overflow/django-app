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
    
    def __init__(self, *args, **kwargs):
        super(TextbookCreationForm, self).__init__(*args, **kwargs)
        self.course_formset = inlineformset_factory(Textbook, Course, form=CourseCreationForm, extra=2, max_num=5)
        self.author_formset = inlineformset_factory(Textbook, Author, form=AuthorCreationForm, extra=2, max_num=5)
        print(f"Course formset extra={self.course_formset.extra}, max_num={self.course_formset.max_num}", flush=True)
        print(f"Author formset extra={self.author_formset.extra}, max_num={self.author_formset.max_num}", flush=True)

class TextbookCopyCreationForm2(ModelForm):
    textbook = TextbookCreationForm()
    
    class Meta:
        model = TextbookCopy
        fields = ['condition', 'for_rent', 'for_sale', 'sale_price', 'rent_price', 'image']
