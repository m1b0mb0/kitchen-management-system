from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from kitchen.models import Cook, Dish, DishIngredient


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience"
        )


class CookUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = (
            "first_name",
            "last_name",
            "years_of_experience"
        )


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = (
            "name",
            "description",
            "price",
            "dish_type",
            "cooks"
        )


DishIngredientFormSet = inlineformset_factory(
    Dish,
    DishIngredient,
    fields=("ingredient", "amount", "unit"),
    extra=1,
    can_delete=True
)
