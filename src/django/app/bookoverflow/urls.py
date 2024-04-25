"""
URL configuration for bookoverflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authentication import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.CustomLogoutView.as_view(template_name='logout.html'), name='logout'),
    path('auth/', include('authentication.urls')),
    path('profile/', include('student_profile.urls')),
    path('textbook/', include('textbook.urls')),
    path('helloworld/', include('helloworld.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('browse/', auth_views.browse, name='browse'),
]
# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
