from django.db import models
from ingredients.models import Ingredient
from recipes.models import Recipe

# Create your models here.
class Recipe_ingredient(models.Model):
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
  ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
  quantity = models.CharField(max_length=10)