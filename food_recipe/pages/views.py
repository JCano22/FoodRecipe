from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from recipes.views import fetch_and_save_recipe
from recipes.models import Recipe
import requests
import random


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cuisines = [
            'American', 'Chinese', 'Indian', 'Italian', 'Mexican', 'Mediterranean'
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

                if response.status_code == 200:
                    data = response.json()
                    hits = data.get('hits', [])

                    if hits:
                        random_recipe = random.choice(hits)['recipe']
                        recipes_to_display.append({
                            'cuisine': cuisine,
                            'title': random_recipe['label'],
                            'ingredients': ', '.join(random_recipe['ingredientLines']),
                            'instructions': random_recipe['url'],
                            'image_url': random_recipe['image'],
                        })
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
        # Recipe.objects.all().delete()

        search_results = fetch_and_save_recipe(search_query)
        return render(request, 'pages/results.html', {'results': search_results, 'search_query': search_query})
    return render(request, 'home.html')


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe
    }
    return render(request, 'pages/detail.html', context)
