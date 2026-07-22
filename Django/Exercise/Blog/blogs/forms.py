"""forms.py is the translation and security layer. It automatically converts our backend database models 
into frontend HTML forms and strictly validates whatever the user types in before it ever touches our database."""

from django import forms
from .models import Blog, Post 

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name']
        labels = {'name': ''}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {'text': ''}