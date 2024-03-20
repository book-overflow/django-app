from django.urls import path
from . import views

urlpatterns = [
	path('profile/', views.profile, name='user-profile'),
    path('setprofile/', views.setProfile),
	path('profile/update', views.updateProfile),
]
