from django.test import TestCase
from .models import User

# Create your tests here.
class UserModelTest(TestCase):
  def setUpTestData():
    # Set up non-modified objects used by all test methods
    User.objects.create(username='joanafm', password='12345xpto')

  def test_username_max_length(self):
    # Get an user object to test
    user = User.objects.get(id=1)

    # Get the metadata for the 'name' field and use it to query its max_length
    max_length = user._meta.get_field('username').max_length

    # Compare the value to the expected result i.e. 30
    self.assertEqual(max_length, 30)

  def test_password_max_length(self):
    # Get an user object to test
    user = User.objects.get(id=1)

    # Get the metadata for the 'name' field and use it to query its max_length
    max_length = user._meta.get_field('password').max_length

    # Compare the value to the expected result i.e. 100
    self.assertEqual(max_length, 100)
  
  def test_user_string_representation(self):
    # Get an user object to test
    user = User.objects.get(id=1)

    #Get ingredient string representation (name)
    user_username = str(user)

    # Compare the value to the expected result i.e. sugar
    self.assertEqual(user_username, 'joanafm')




  