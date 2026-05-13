from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q
from django.urls import reverse_lazy
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from kitchen.models import Cook, DishType, Dish, Ingredient
from kitchen.forms import (
    CookCreationForm,
    CookUpdateForm,
    DishForm,
    DishIngredientFormSet,
    CookSearchForm,
    DishTypeSearchForm,
    DishSearchForm,
    IngredientSearchForm
)


class SearchMixin:
    search_form_class = None
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.search_form_class(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data.get("query")

            if query:
                q_objects = Q()
                for field in self.search_fields:
                    q_objects |= Q(**{f"{field}__icontains": query})

                queryset = queryset.filter(q_objects)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form_class(self.request.GET)
        return context


@login_required
def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_cooks": Cook.objects.count(),
        "num_dish_types": DishType.objects.count(),
        "num_dishes": Dish.objects.count(),
        "num_ingredients": Ingredient.objects.count()
    }
    return render(request, "kitchen/index.html", context=context)


class IngredientListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Ingredient
    search_form_class = IngredientSearchForm
    search_fields = ["name"]
    paginate_by = 5


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = DishType
    search_form_class = DishTypeSearchForm
    search_fields = ["name"]
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["dish_ingredients"] = DishIngredientFormSet(
                self.request.POST,
                prefix="dish_ingredients"
            )
        else:
            context["dish_ingredients"] = DishIngredientFormSet(
                prefix="dish_ingredients"
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        dish_ingredients = context["dish_ingredients"]

        with transaction.atomic():
            self.object = form.save()

            if dish_ingredients.is_valid():
                dish_ingredients.instance = self.object
                dish_ingredients.save()
            else:
                return self.form_invalid(form)
        return super().form_valid(form)


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["dish_ingredients"] = DishIngredientFormSet(
                self.request.POST,
                instance=self.object,
                prefix="dish_ingredients"
            )
        else:
            context["dish_ingredients"] = DishIngredientFormSet(
                instance=self.object,
                prefix="dish_ingredients"
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        dish_ingredients = context["dish_ingredients"]

        with transaction.atomic():
            self.object = form.save()

            if dish_ingredients.is_valid():
                dish_ingredients.instance = self.object
                dish_ingredients.save()
            else:
                return self.form_invalid(form)
        return redirect(self.success_url)


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class DishListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type")
    search_form_class = DishSearchForm
    search_fields = ["name"]
    paginate_by = 5


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    queryset = Dish.objects.select_related(
        "dish_type"
    ).prefetch_related(
        "dish_ingredients__ingredient"
    )


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


class CookListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Cook
    search_form_class = CookSearchForm
    search_fields = ["username"]
    paginate_by = 5


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("dishes__dish_type")


class ToggleCookAssignmentView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        cook = self.request.user
        dish = Dish.objects.get(id=pk)
        if dish.cooks.filter(pk=cook.pk).exists():
            dish.cooks.remove(cook)
        else:
            dish.cooks.add(cook)
        
        return redirect("kitchen:dish-detail", pk=dish.pk)
