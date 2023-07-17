from django.test import TestCase
from .models import Note, User, Recipe

# Create your tests here.
class NoteModelTest(TestCase):
  def setUpTestData():
    # Set up non-modified objects used by all test methods
    user = User.objects.create(username='joanafm', password='12345xpto')
    recipe = Recipe.objects.create(user_id = User.objects.get(id=1), name='Lemonade', cooking_time=5)
    Note.objects.create(user_id = User.objects.get(id=1), recipe_id = Recipe.objects.get(id=1), user_note='Add more flour.')

  def test_note_user(self):
    note = Note.objects.get(id=1)
    self.assertEqual(note.user_id.username, 'joanafm')

  def test_note_recipe(self):
    note = Note.objects.get(id=1)
    self.assertEqual(note.recipe_id.name, 'Lemonade')
