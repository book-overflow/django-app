from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(University)
admin.site.register(Course)
admin.site.register(Author)
admin.site.register(Textbook)
admin.site.register(TextbookCopy)
admin.site.register(Transaction)