from recipes.models import Recipe    #you need to connect parameters from recipes model
from io import BytesIO 
import base64
import matplotlib.pyplot as plt

#define a function that takes the ID
def get_recipe_link_from_id(val):
   #this ID is used to retrieve the link and name from the record
   recipe = Recipe.objects.get(id=val)
   recipe_link ='<a href="/recipes/list/' + str(recipe.id) + '">' + recipe.name + '</a>'
   #and the link is returned back
   return recipe_link

def get_recipe_cooking_time_interval(val):
  recipe = Recipe.objects.get(id=val)

  if recipe.cooking_time <= 15:
    return '0-15'
  elif recipe.cooking_time <= 30:
    return '16-30'
  elif recipe.cooking_time <= 45:
    return '31-45'
  else:
    return '> 45'
  
def get_recipe_num_ingredients(val):
  recipe = Recipe.objects.get(id=val)

  return recipe.ingredients.count()

def get_recipe_pic_anchor(val):
  recipe = Recipe.objects.get(id=val)
  return '<img src="' + recipe.pic.url + '" alt="' + recipe.name + '" />'

def get_graph():
  #create a BytesIO buffer for the image
  buffer = BytesIO()         

  #create a plot with a bytesIO object as a file-like object. Set format to png
  plt.savefig(buffer, format='png')

  #set cursor to the beginning of the stream
  buffer.seek(0)

  #retrieve the content of the file
  image_png=buffer.getvalue()

  #encode the bytes-like object
  graph=base64.b64encode(image_png)

  #decode to get the string as output
  graph=graph.decode('utf-8')

  #free up the memory of buffer
  buffer.close()

  #return the image/graph
  return graph

#chart_type: user input o type of chart,
#data: pandas dataframe
def get_chart(chart_type, data, **kwargs):
  #switch plot backend to AGG (Anti-Grain Geometry) - to write to file
  #AGG is preferred solution to write PNG files
  plt.switch_backend('AGG')

  #specify figure size
  fig=plt.figure(figsize=(6,3))

  #select chart_type based on user input from the form
  if chart_type == '#1':
    n_by_time = data.groupby('cooking_time_interval')['cooking_time_interval'].size().reset_index(name='count')
    #plot bar chart between cooking time (less or equal to 15 minutes, less or equal to 30 minutes and less or equal to 45 minutes and greater than 45 minutes) on x-axis and number of recipes on y-axis
    plt.bar(n_by_time['cooking_time_interval'], n_by_time['count'])
    plt.ylabel('Number of recipes')
    plt.xlabel('Cooking time (minutes)')
  elif chart_type == '#2':
    #generate pie chart based on the difficulty.
    n_by_difficulty = data.groupby('difficulty')['difficulty'].size().reset_index(name='count')
    plt.pie(n_by_difficulty['count'], labels = n_by_difficulty['difficulty'])
  elif chart_type == '#3':
    n_by_ingredients = data.groupby('num_ingredients')['num_ingredients'].size().reset_index(name='count')
    #plot Line chart between number of ingredients on x-axis and number of recipes on y-axis
    plt.plot(n_by_ingredients['num_ingredients'], n_by_ingredients['count'])
    plt.ylabel('Number of recipes')
    plt.xlabel('Number of ingredients')
  else:
    print ('unknown chart type')

  #specify layout details
  plt.tight_layout()

  #render the graph to file
  chart =get_graph() 
  return chart       