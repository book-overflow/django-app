from django.urls import path
from . import views

urlpatterns = [
	path('', views.getProfile, name='get-profile'),
	path('create', views.createProfile, name='create-profile'),
	path('update', views.updateProfile, name='update-profile')
]
