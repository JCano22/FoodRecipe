from django.shortcuts import render
from .models import Recipe
import requests


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
                )
                recipes_to_save.append(new_recipe)

        # adds recipes_to_save to db all at once
        Recipe.objects.bulk_create(recipes_to_save)

        return recipes_to_save
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the API request

        print(f"Error fetching recipes: {e}")
        return None
