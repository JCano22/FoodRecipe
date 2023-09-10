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

        # call the db again to retrieve the product (with id)
        titles = [r.title for r in recipes_to_save]
        results = Recipe.objects.filter(title__in=titles)

        next_page_url = recipe_data['_links'].get('next', {}).get('href', None)

        return results, next_page_url
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the API request

        print(f"Error fetching recipes: {e}")
        return None


@method_decorator(csrf_protect, name='dispatch')
class SaveNextView(View):
    def post(self, request):
        recipe_data = json.loads(request.body)
        recipes_to_save = []

        try:
            for recipe_info in recipe_data:
                recipe_json = recipe_info['recipe']
                new_recipe = Recipe(
                    title=recipe_json['label'],
                    ingredients='\n'.join(recipe_json['ingredientLines']),
                    instructions=recipe_json['url'],
                    image_url=recipe_json['images']['REGULAR']['url'],
                    calories=recipe_json['calories'],
                    cuisine=recipe_json['cuisineType'],
                    health=recipe_json['healthLabels'],
                )
                recipes_to_save.append(new_recipe)

            Recipe.objects.bulk_create(recipes_to_save)
            saved_recipes_info = [{
                'id': recipe.id, 'title': recipe.title,
                'image_url': recipe.image_url} for recipe in recipes_to_save]
            return JsonResponse(saved_recipes_info, safe=False)
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError as e:
            print("KeyError:", e)
            return JsonResponse({'error': 'Missing key in JSON data'}, status=400)


def fetch_and_save_filter(search_query, health, cuisine):
    api_endpoint = 'https://api.edamam.com/api/recipes/v2'
    app_id = '89066d53'
    app_key = 'aaeb814a753085a9345d83ed37bf2ee6'

    if cuisine and health:
        params = {
            'type': 'public',
            'q': search_query,
            'app_id': app_id,
            'app_key': app_key,
            'health': health,
            'cuisineType': cuisine,
        }
    elif health:
        params = {
            'type': 'public',
            'q': search_query,
            'app_id': app_id,
            'app_key': app_key,
            'health': health,
        }
    elif cuisine:
        params = {
            'type': 'public',
            'q': search_query,
            'app_id': app_id,
            'app_key': app_key,
            'cuisineType': cuisine,
        }
    else:
        params = {
            'type': 'public',
            'q': search_query,
            'app_id': app_id,
            'app_key': app_key,
            'cuisineType': cuisine,
        }

    try:
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()  # to check for errors
        recipe_data = response.json()

        recipes_to_save = []

        for recipe_info in recipe_data['hits']:
            recipe = recipe_info['recipe']

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

        Recipe.objects.bulk_create(recipes_to_save)

        next_page_url = recipe_data['_links'].get('next', {}).get('href', None)
        print("from the filter fetch!!!")
        print(next_page_url)

        return recipes_to_save, next_page_url
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the API request

        print(f"Error fetching recipes: {e}")
        return None
