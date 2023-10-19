from django.shortcuts import render, redirect
from .forms import InsertIngredients
import requests
from django.contrib.auth.decorators import login_required
from .models import Nutrient


api_key = '99aa443bda864d698ad5ac6db226c843'
url = "https://api.spoonacular.com/recipes"


@login_required(login_url='/login')
def home(request):
    titles, images, ids, readyInMinutes, servings = [], [], [], [], []
    r = requests.get(f'{url}/random?apiKey={api_key}&tags=lunch&number=9').json()
    r = r['recipes']
    for index, item in enumerate(r):
        if 'image' in r[index]:
            titles.append(r[index]['title'])
            images.append(r[index]['image'])
            ids.append(r[index]['id'])
            readyInMinutes.append(r[index]['readyInMinutes'])
            servings.append(r[index]['servings'])
    items = zip(titles, images, ids, readyInMinutes, servings)
    context = {'items': items}
    return render(request, 'recipes/home.html', context)


@login_required(login_url='/login')
def detail_recipes(request, pk):
    r = requests.get(f'{url}/{pk}/information?apiKey={api_key}&'
                     f'includeNutrition=false').json()
    sourceURL = r['sourceUrl']
    return redirect(sourceURL)


@login_required(login_url='/login')
def ingredients_recipes(request):
    if request.method == 'POST':
        titles, images, ids = [], [], []
        conditionals = 'number=6&ranking=1&ignorePantry=false'
        ingredients = request.POST.get('ingredients')
        r = requests.get(f'{url}/findByIngredients?apiKey={api_key}&'
                         f'{conditionals}&'
                         f'ingredients={ingredients}').json()
        for index, item in enumerate(r):
            titles.append(r[index]['title'])
            images.append(r[index]['image'])
            ids.append(r[index]['id'])
        items = zip(titles, images, ids)
        context = {'items': items}
        return render(request, 'recipes/recipes_from_ingredients.html', context)
    else:
        form = InsertIngredients()
        context = {'form': form}
        return render(request, 'recipes/insert_ingredients.html', context)


@login_required(login_url='/login')
def requirements_recipes(request):
    if request.method == 'POST':
        titles, images, ids = [], [], []
        query = ''
        for key, value in request.POST.items():
            if key.startswith('selected_option_'):
                key = key.replace('selected_option_', '')
                query += f'&{key}={value}'
        try:
            r = requests.get(f'{url}/findByNutrients?apiKey={api_key}&number=9&random=true{query}').json()
        except:
            nutrients = Nutrient.objects.all()
            error_message = 'Something in Your choices is not right. Please try again.'
            context = {'nutrients': nutrients, 'error_message': error_message}
            return render(request, 'recipes/insert_requirements.html', context)
        else:

            for index, item in enumerate(r):
                titles.append(r[index]['title'])
                images.append(r[index]['image'])
                ids.append(r[index]['id'])
            items = zip(titles, images, ids)
            context = {'items': items}
            return render(request, 'recipes/recipes_from_requirements.html', context)
    else:
        nutrients = Nutrient.objects.all()
        context = {'nutrients': nutrients}
        return render(request, 'recipes/insert_requirements.html', context)
