from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Textbook

def textbook_list(request):
    textbooks = Textbook.objects.all()
    return render(request, 'textbook/textbook_list.html', {'textbooks': textbooks})

def textbook_detail(request, textbook_id):
    textbook = get_object_or_404(Textbook, pk=textbook_id)
    return render(request, 'textbook/textbook_detail.html', {'textbook': textbook})
