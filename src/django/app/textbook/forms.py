from django.forms import ModelForm
from shared.models import Course, Author, Textbook, TextbookCopy

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'name', 'description']

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']

class TextbookForm(ModelForm):
    class Meta:
        model = Textbook
        fields = ['isbn', 'title', 'edition']

class TextbookCopyForm(ModelForm):
    class Meta:
        model = TextbookCopy
        fields = ['condition', 'for_rent', 'for_sale', 'sale_price', 'rent_price', 'image']
