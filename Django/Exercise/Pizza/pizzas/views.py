from django.shortcuts import render
from .models import Pizza, Toppings


def index(request):
    """The home page for Pizza App"""
    return render(request, 'pizzas/index.html')

def pizzas(request):
    """Show all the Pizzas"""
    pizzas = Pizza.objects.all()    # returns all the pizzas
    context = {'pizzas': pizzas}
    return render(request, 'pizzas/pizzas.html', context)

def pizza(request, pizza_id):
    """Show a single pizza and all its toppings."""
    # These two lines are called queries for the database
    pizza = Pizza.objects.get(id=pizza_id)  # 1
    toppings =  pizza.toppings_set.all()# returns the toppings related to the pizza, the name
                                        # toppings_set is made from the name Toppings (which is the class)
                                        # lowercase(name_of_class) + '_set'
    context = {'pizza': pizza, 'toppings': toppings}
    return render(request, 'pizzas/pizza.html', context)