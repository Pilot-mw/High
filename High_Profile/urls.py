"""
URL configuration for High_Profile project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
]
