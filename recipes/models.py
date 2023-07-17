from django.db import models
from ingredients.models import Ingredient
from users.models import User
#from recipe_ingredients.models import Recipe_ingredient
from django.shortcuts import reverse

# Create your models here.
difficulty_choices = (
  ('easy', 'Easy'),
  ('medium', 'Medium'),
  ('intermediate', 'Intermediate'),
  ('hard', 'Hard'),
)

class Recipe(models.Model):
  name = models.CharField(max_length=50)
  ingredients = models.ManyToManyField(Ingredient, through='recipe_ingredients.Recipe_ingredient', through_fields=('recipe', 'ingredient'))
  cooking_time = models.IntegerField(help_text='Cooking time in minutes')
  difficulty = models.CharField(max_length=20, choices=difficulty_choices)
  pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')
  method = models.TextField(default='No method')
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.name)
  
  def get_absolute_url(self):
    return reverse ('recipes:detail', kwargs={'pk': self.pk})
  
  def get_difficulty(self):
    ingredient_count = self.ingredients.count()

    if self.cooking_time < 10 and ingredient_count < 4:
      difficulty = 'Easy' 
    elif self.cooking_time < 10 and ingredient_count >= 4:
      difficulty = 'Medium'
    elif self.cooking_time >= 10 and ingredient_count < 4:
      difficulty = 'Intermediate'
    elif self.cooking_time >= 10 and ingredient_count >= 4:
      difficulty = 'Hard'
    else:
      difficulty = 'Unknown'
  
    return difficulty
