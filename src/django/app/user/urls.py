from django.urls import path
from student_profile import views as profile_views
from textbook import views as textbook_views

urlpatterns = [
	path('profile', profile_views.getProfile, name='get-profile'),
	path('profile/create', profile_views.createProfile, name='create-profile'),
	path('profile/update', profile_views.updateProfile, name='update-profile'),
    path('textbooks', textbook_views.getUserListings, name='get-user-listings'),
    path('textbooks/<int:id>', textbook_views.getUserListing, name='get-user-listing'),
	path('textbooks/delete/<int:id>', textbook_views.deleteUserListing, name='delete-user-listing'),
	path('textbooks/create', textbook_views.createListing, name='create-listing'),
	# path('textbooks/<int:id>/update', textbook_views.updateListing, name='update-listing')
]
