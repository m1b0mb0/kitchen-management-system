from django.urls import path

from kitchen.views import (
    index,
    IngredientListView,
    DishTypeListView,
    DishListView,
    DishDetailView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    CookListView,
    CookDetailView,
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
    path(
        "dishes/<int:pk>/",
        DishDetailView.as_view(),
        name="dish-detail"
    ),
    path(
        "cooks/create/",
        CookCreateView.as_view(),
        name="cook-create"
    ),
    path(
        "cooks/<int:pk>/update/",
        CookUpdateView.as_view(),
        name="cook-update"
    ),
    path(
        "cooks/<int:pk>/delete/",
        CookDeleteView.as_view(),
        name="cook-delete"
    ),
    path(
        "cooks/",
        CookListView.as_view(),
        name="cook-list"
    ),
    path(
        "cooks/<int:pk>/",
        CookDetailView.as_view(),
        name="cook-detail"
    ),
]

app_name = "kitchen"
