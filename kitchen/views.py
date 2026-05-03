from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from kitchen.models import Cook, DishType, Dish, Ingredient


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_cooks": Cook.objects.count(),
        "num_dish_types": DishType.objects.count(),
        "num_dishes": Dish.objects.count(),
        "num_ingredients": Ingredient.objects.count()
    }
    return render(request, "kitchen/index.html", context=context)
