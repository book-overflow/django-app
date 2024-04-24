from django.urls import path
from . import views

urlpatterns = [
    path('', views.getMyTextbooks, name='my-textbooks'),
	path('newPost', views.createPost, name='create-post'),
    path('getPost', views.getPost, name='get-post'),
]
