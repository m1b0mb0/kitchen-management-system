from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator


class Cook(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(50)],
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField(
        "Ingredient",
        through="DishIngredient"
    )

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "dishes"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("kitchen:dish-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class DishIngredient(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="dish_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="dish_ingredients"
    )
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    unit = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["dish", "ingredient"],
                name="unique_dish_ingredient"
            )
        ]
