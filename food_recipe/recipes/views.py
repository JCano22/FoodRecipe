from django.shortcuts import render
from .models import Recipe
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
import json


# Create your views here.

# view function to fetch data from API and store to db
def fetch_and_save_recipe(search_query):
    api_endpoint = 'https://api.edamam.com/api/recipes/v2'
    app_id = '89066d53'
    app_key = 'aaeb814a753085a9345d83ed37bf2ee6'

    params = {
        'type': 'public',
        'q': search_query,
        'app_id': app_id,
        'app_key': app_key,
    }

    try:
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()  # to check for errors
        recipe_data = response.json()

        recipes_to_save = []

        for recipe_info in recipe_data['hits']:
            recipe = recipe_info['recipe']
            recipeImg = recipe['images']['REGULAR']['url']

            if recipeImg:
                new_recipe = Recipe(
                    title=recipe['label'],
                    ingredients='\n'.join(recipe['ingredientLines']),
                    instructions=recipe['url'],
                    image_url=recipe['images']['REGULAR']['url'],
                    calories=recipe['calories'],
                    cuisine=recipe['cuisineType'],
                    health=recipe['healthLabels'],
                )
                recipes_to_save.append(new_recipe)
            else:
                new_recipe = Recipe(
                    title=recipe['label'],
                    ingredients='\n'.join(recipe['ingredientLines']),
                    instructions=recipe['url'],
                    image_url="./static/media/noImage.jpg",
                    calories=recipe['calories'],
                    cuisine=recipe['cuisineType'],
                    health=recipe['healthLabels'],
                )
                recipes_to_save.append(new_recipe)

        # adds recipes_to_save to db all at once
        Recipe.objects.bulk_create(recipes_to_save)

        next_page_url = recipe_data['_links'].get('next', {}).get('href', None)
        print("From fetch and save method:", next_page_url)

        return recipes_to_save, next_page_url
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the API request

        print(f"Error fetching recipes: {e}")
        return None


@method_decorator(csrf_protect, name='dispatch')
class SaveRecipeView(View):
    def post(self, request):
        recipe_data = request.body.decode('utf-8')
        try:
            recipe_json = json.loads(recipe_data)
            new_recipe = Recipe(
                title=recipe_json['title'],
                ingredients=recipe_json['ingredients'],
                instructions=recipe_json['instructions'],
                image_url=recipe_json['image_url'],
                calories=recipe_json['calories'],
                cuisine=recipe_json['cuisine'],
                health=recipe_json['health'],
            )
            new_recipe.save()
            return JsonResponse({'message': 'Recipe saved successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': 'Missing key in JSON data'}, status=400)
