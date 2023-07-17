from django.test import TestCase
from .models import Recipe_ingredient, Ingredient, Recipe
from users.models import User

# Create your tests here.
class Recipe_ingredientModelTest(TestCase):
  def setUpTestData():
    # Set up non-modified objects used by all test methods
    User.objects.create(username='joanafm', password='12345xpto')
    ingredient = Ingredient.objects.create(name='Lemons')
    recipe = Recipe.objects.create(user_id = User.objects.get(id=1), name='Lemonade', cooking_time=5)
    Recipe_ingredient.objects.create(ingredient = Ingredient.objects.get(id=1), recipe = Recipe.objects.get(id=1), quantity='150 g')

  def test_recipe_ingredient_in_recipe(self):
    recipe = Recipe.objects.get(id=1)
    ingredient = recipe.ingredients.get(id=1)
    self.assertEqual(ingredient.name, 'Lemons')
  
  def test_recipe_ingredient_quantity_max_length(self):
    # Get a recipe ingredient object to test
    recipe_ingredient = Recipe_ingredient.objects.get(id=1)

    # Get the metadata for the 'quantity' field and use it to query its max_length
    max_length = recipe_ingredient._meta.get_field('quantity').max_length

    # Compare the value to the expected result i.e. 10
    self.assertEqual(max_length, 10)