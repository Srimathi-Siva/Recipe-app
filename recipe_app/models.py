# recipe_app/models.py (assuming your app is named 'recipe_app')

from django.db import models
from django.utils import timezone

class Recipe(models.Model):
    """
    Represents a single recipe.
    """
    id = models.AutoField(primary_key=True) # AutoField for auto-incrementing integer ID
    name = models.CharField(max_length=255, help_text="The name of the recipe.")
    description = models.TextField(blank=True, help_text="A detailed description of the recipe.")
    instructions = models.TextField(help_text="Step-by-step instructions for preparing the recipe.")
    prep_time_minutes = models.IntegerField(
        null=True, blank=True,
        help_text="Estimated preparation time in minutes."
    )
    cook_time_minutes = models.IntegerField(
        null=True, blank=True,
        help_text="Estimated cooking time in minutes."
    )
    servings = models.IntegerField(
        null=True, blank=True,
        help_text="Number of servings the recipe yields."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time the recipe was added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time the recipe was last modified.")

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ['name'] # Order recipes by name by default

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """
    Represents a single ingredient.
    """
    id = models.AutoField(primary_key=True) # AutoField for auto-incrementing integer ID
    name = models.CharField(max_length=100, unique=True, help_text="The name of the ingredient (e.g., 'Salt', 'Sugar').")
    # unit is a suggested common unit for the ingredient, actual unit for a recipe is in RecipeIngredient
    unit = models.CharField(
        max_length=50, blank=True,
        help_text="A common unit for the ingredient (e.g., 'grams', 'ml', 'cup'). Optional."
    )

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ['name'] # Order ingredients by name by default

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    """
    A through model that links Recipe and Ingredient,
    specifying the quantity and unit of an ingredient for a specific recipe.
    """
    id = models.AutoField(primary_key=True) # AutoField for auto-incrementing integer ID
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        help_text="The recipe this ingredient belongs to."
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        help_text="The ingredient used in this recipe."
    )
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="The amount of the ingredient needed for the recipe."
    )
    unit = models.CharField(
        max_length=50,
        help_text="The specific unit for this ingredient in *this* recipe (e.g., 'grams', 'cups', 'large')."
    )
    notes = models.CharField(
        max_length=255, blank=True,
        help_text="Any specific notes about this ingredient for the recipe (e.g., 'chopped', 'finely diced'). Optional."
    )

    class Meta:
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe Ingredients"
        # Ensure that an ingredient can only be listed once per recipe
        unique_together = ('recipe', 'ingredient')
        ordering = ['recipe', 'ingredient__name'] # Order by recipe, then ingredient name

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} for {self.recipe.name}"

