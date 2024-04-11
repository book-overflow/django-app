from django.urls import path
from . import views


urlpatterns = [
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
]
