from django.urls import path
from . import views

urlpatterns = [
    path('', views.getMyTextbooks, name='my-textbooks'),
	path('newPost2', views.createPost2, name='create-post-2'),
	path('newPost', views.createPost, name='create-post'),
    path('getPost', views.getPost, name='get-post'),
]
