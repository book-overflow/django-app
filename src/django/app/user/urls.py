from django.urls import path
from . import views
from .views import register, login  # Import the register view


urlpatterns = [
    path("profile/", views.getProfile, name="user-profile"),
    path("profile/update", views.updateProfile, name="user-profile-update"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
]
