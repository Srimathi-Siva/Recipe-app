# recipe_app/admin.py

from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)