from django.shortcuts import render
from django.views.generic import ListView, DetailView #to display lists and details
from .models import Recipe #to access Recipe model
from django.contrib.auth.mixins import LoginRequiredMixin #to protect class-based view
from .forms import RecipesSearchForm
from .models import Recipe

import pandas as pd

from .utils import get_recipe_link_from_id, get_recipe_cooking_time_interval, get_recipe_num_ingredients, get_chart, get_recipe_pic_anchor

# Create your views here.
# def recipes_home(request):
#    return render(request, 'recipes/recipes_home.html')

class HomeRecipeListView(LoginRequiredMixin,ListView):             #class-based “protected” view
   model = Recipe                               #specify model
   template_name = 'recipes/recipes_home.html'  #specify template 

class RecipeListView(LoginRequiredMixin, ListView):           #class-based “protected” view
   model = Recipe                         #specify model
   template_name = 'recipes/main.html'    #specify template 

class RecipeDetailView(LoginRequiredMixin, DetailView):                       #class-based “protected” view
   model = Recipe                                       #specify model
   template_name = 'recipes/detail.html'                 #specify template

#define function-based view - recipes()
def records(request):
   #create an instance of RecipesSearchForm that you defined in recipes/forms.py
   form = RecipesSearchForm(request.POST or None)
   recipes_df=None     #initialize dataframe to None
   chart = None

   #check if the button is clicked
   if request.method =='POST':
      #read recipe_name and chart_type
      recipe_name = request.POST.get('recipe_name')
      max_cooking_time = request.POST.get('max_cooking_time')
      difficulty = request.POST.get('difficulty')
      chart_type = request.POST.get('chart_type')
      ingredient = request.POST.get('ingredient')
      #display in terminal - needed for debugging during development only
      print (recipe_name, max_cooking_time, difficulty, chart_type)

      #apply filter to extract data
      qs = Recipe.objects.filter(name__contains=recipe_name)
      if max_cooking_time.isdigit() and int(max_cooking_time) > 0:
         qs = qs.filter(cooking_time__lte=max_cooking_time)
      
      if difficulty != '0':
         qs = qs.filter(difficulty=difficulty)

      # if ingredient != '':
      #    qs = qs.filter(.contains)

      if qs:      #if data found
         #convert the queryset values to pandas dataframe
         recipes_df=pd.DataFrame(qs.values())

         #convert the ID to Link of recipe
         #recipes_df['name']='<a href="/recipes/list/' + str(recipes_df['id']) + '">' + recipes_df['name'] + '</a>'
         
         recipes_df['name']=recipes_df['id'].apply(get_recipe_link_from_id)
         
         #create new columns for charts
         recipes_df['cooking_time_interval'] = recipes_df['id'].apply(get_recipe_cooking_time_interval)

         recipes_df['num_ingredients'] = recipes_df['id'].apply(get_recipe_num_ingredients)

         recipes_df['pic'] = recipes_df['id'].apply(get_recipe_pic_anchor)


         #call get_chart by passing chart_type from user input, sales dataframe and labels
         chart=get_chart(chart_type, recipes_df)

         #convert the dataframe to HTML
         recipes_df=recipes_df.to_html(escape=False) 

      """ print ('Exploring querysets:')
      print ('Case 1: Output of Recipe.objects.all()')
      qs = Recipe.objects.all()
      print (qs)

      print ('Case 2: Output of Recipe.objects.filter(name=recipe_name)')
      qs =Recipe.objects.filter(name=recipe_name)
      print (qs)

      print ('Case 3: Output of qs.values')
      print (qs.values())

      print ('Case 4: Output of qs.values_list()')
      print (qs.values_list())

      print ('Case 5: Output of Recipe.objects.get(id=1)')
      obj = Recipe.objects.get(id=1)
      print (obj) """

   #pack up data to be sent to template in the context dictionary
   context={
      'form': form,
      'recipes_df': recipes_df,
      'chart': chart
   }

   #load the recipes/main.html page using the data that you just prepared
   return render(request, 'recipes/records.html', context)