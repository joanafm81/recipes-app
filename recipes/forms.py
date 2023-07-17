from django import forms

CHART__CHOICES = (        #specify choices as a tuple
  ('#1', 'Bar chart'),    # when user selects "Bar chart", it is stored as "#1"
  ('#2', 'Pie chart'),
  ('#3', 'Line chart')
)

DIFFICULTY__CHOICES = (
  ('0', '(any)'),
  ('easy', 'Easy'),
  ('medium', 'Medium'),
  ('intermediate', 'Intermediate'),
  ('hard', 'Hard'),
)

#define class-based Form imported from Django forms
class RecipesSearchForm(forms.Form): 
  recipe_name = forms.CharField(max_length=120, required=False)
  ingredient = forms.CharField(max_length=50, required=False)
  max_cooking_time = forms.IntegerField(required=False)
  difficulty = forms.ChoiceField(choices=DIFFICULTY__CHOICES, required=False)
  chart_type = forms.ChoiceField(choices=CHART__CHOICES)