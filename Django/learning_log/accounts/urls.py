"""Defines URL patterns for accounts."""
from django.urls import path, include

app_name = 'accounts'
urlpatterns = [
# Include default auth urls.
path('', include('django.contrib.auth.urls')),
# django.contrib.auth.urls: This is a built-in Django module containing pre-written URL
# patterns for common user tasks (login, logout, password resets).
]
