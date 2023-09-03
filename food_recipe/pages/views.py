from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from recipes.views import fetch_and_save_recipe, fetch_and_save_filter
from recipes.models import Recipe
from saved_recipes.models import SavedRecipe
import requests
import random
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cuisines = [
            'American', 'Chinese', 'Indian', 'Italian', 'Mexican', 'Mediterranean', 'French', 'Asian'
        ]
        recipes_to_display = []
        for cuisine in cuisines:
            # Make API request to Edamam to get random recipes for the selected cuisine
            api_endpoint = 'https://api.edamam.com/api/recipes/v2'
            app_id = '89066d53'
            app_key = 'aaeb814a753085a9345d83ed37bf2ee6'

            params = {
                'type': 'public',
                'app_id': app_id,
                'app_key': app_key,
                'cuisineType': cuisine,
            }
            try:
                response = requests.get(api_endpoint, params=params)
                response.raise_for_status()
                data = response.json()
                hits = data.get('hits', [])

                if hits:
                    random_recipe = random.choice(hits)['recipe']

                    recipe_instance = Recipe(
                        title=random_recipe['label'],
                        ingredients='\n'.join(
                            random_recipe['ingredientLines']),
                        instructions=random_recipe['url'],
                        image_url=random_recipe['image'],
                        calories=random_recipe['calories'],
                        cuisine=cuisine,
                    )

                    recipes_to_display.append(recipe_instance)
                    recipe_instance.save()
            except requests.exceptions.RequestException as e:
                # Handle any errors that occur during the API request
                print(f"Error fetching recipes: {e}")
                return None

        context['recipes_to_display'] = recipes_to_display
        return context


# view function to search api with keyword from user
def search_recipes(request):
    if request.method == 'POST':

        search_query = request.POST.get('search_query', '')
        print(search_query)
        # Recipe.objects.all().delete()

        # retrieves ids for savedrecipe objects
        saved_recipe_ids = SavedRecipe.objects.values_list(
            'recipe_id', flat=True)
        # Delete recipes that are not saved by any user
        Recipe.objects.exclude(id__in=saved_recipe_ids).delete()

        search_results, next_page_url = fetch_and_save_recipe(
            search_query)

        context = {
            'results': search_results,
            'search_query': search_query,
            'next_page': next_page_url,
        }

        return render(request, 'pages/results.html', context)

    return render(request, 'home.html')


def search_filter(request):
    if request.method == 'POST':
        health_labels = request.POST.getlist('healthLabel', '')
        cuisine = request.POST.get('cuisineType', '')
        search_query = request.POST.get('searchQ', '')

        filterResults, next_page_url = fetch_and_save_filter(
            search_query, health_labels, cuisine, )

        context = {
            'results': filterResults,
            'search_query': search_query,
            'next_page': next_page_url
        }

        return render(request, 'pages/results.html', context)


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe
    }
    return render(request, 'pages/detail.html', context)
