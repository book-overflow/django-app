from django import forms
from django.forms import ModelForm
from shared.models import TextbookCopy

class TextbookCopyCreationForm(ModelForm):
    isbn = forms.IntegerField()
    name = forms.CharField(max_length=255)
    authors = forms.CharField(max_length=255)
    course = forms.CharField(max_length=255)
    edition = forms.IntegerField()
    class Meta:
        model = TextbookCopy
        fields = ['condition', 'for_rent', 'for_sale', 'sale_price', 'rent_price', 'image']
