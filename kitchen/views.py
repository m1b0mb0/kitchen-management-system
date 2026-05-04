from django.shortcuts import render
from django.views import generic
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


class IngredientListView(generic.ListView):
    model = Ingredient


class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"


class DishListView(generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type")


class DishDetailView(generic.DetailView):
    model = Dish
    queryset = Dish.objects.select_related(
        "dish_type"
    ).prefetch_related(
        "dish_ingredients__ingredient"
    )


class CookListView(generic.ListView):
    model = Cook


class CookDetailView(generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("dishes__dish_type")
