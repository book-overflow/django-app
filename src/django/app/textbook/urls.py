from django.urls import path
from . import views

urlpatterns = [
    path('', views.getListings, name='get-listings'),
    path('<int:id>', views.getListing, name='get-listing')
]
