from django.contrib import admin

from .models import Pizza
from .models import Toppings

admin.site.register(Pizza)
admin.site.register(Toppings)