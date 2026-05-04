from django.urls import path

from kitchen.views import (
    index,
    IngredientListView,
    DishTypeListView,
    DishListView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "ingredients/",
        IngredientListView.as_view(),
        name="ingredient-list"
    ),
    path(
        "dish-types/",
        DishTypeListView.as_view(),
        name="dish-type-list"
    ),
    path(
        "dishes/",
        DishListView.as_view(),
        name="dish-list"
    ),
]

app_name = "kitchen"
