"""Define URL patterns for blog"""
from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # New-Blog page
    path('new_blog/', views.new_blog, name='new_blog'),
    # New-Post page
    path('new_post/<int:blog_id>/', views.new_post, name='new_post'),
    # Editing-Post page
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    # Blog page
    path('blog/<int:blog_id>/', views.blog, name='blog'),
]