from django.urls import path

from kitchen.views import index, IngredientListView

urlpatterns = [
    path("", index, name="index"),
    path(
        "ingredients/",
        IngredientListView.as_view(),
        name="ingredient-list"
    ),
]

app_name = "kitchen"