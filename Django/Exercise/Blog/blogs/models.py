from django.db import models

# Create your models here.

class Blog(models.Model):
    """A Blog the user is writing/ about"""
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model"""
        return self.name

class Post(models.Model):
    """Something about the Blog"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model"""
        return f"{self.text[:50]}..."