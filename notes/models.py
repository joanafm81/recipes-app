from django.db import models
from users.models import User
from recipes.models import Recipe

# Create your models here.
class Note(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
  user_note = models.TextField(default='No notes')

  def __str__(self):
    return str(self.user_note)