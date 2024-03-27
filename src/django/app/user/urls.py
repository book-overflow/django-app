from django.urls import path
from . import views

urlpatterns = [
	path('profile/', views.getProfile, name='user-profile'),
	path('profile/update', views.updateProfile, name='user-profile-update'),
]
