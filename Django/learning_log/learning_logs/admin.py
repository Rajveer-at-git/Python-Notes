from django.contrib import admin

# The dot in front of models tells Django to
# look for models.py in the same directory as admin.py
from .models import Topic
from .models import Entry

admin.site.register(Topic)
admin.site.register(Entry)