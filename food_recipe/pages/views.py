from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from recipes.views import fetch_and_save_recipe, fetch_and_save_next_page
from recipes.models import Recipe
from saved_recipes.models import SavedRecipe
import requests
import random
from django.contrib.auth.decorators import login_required


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
        # Recipe.objects.all().delete()

        # retrieves ids for savedrecipe objects
        saved_recipe_ids = SavedRecipe.objects.values_list(
            'recipe_id', flat=True)
        # Delete recipes that are not saved by any user
        Recipe.objects.exclude(id__in=saved_recipe_ids).delete()

        search_results, next_page_url, current_page_url, previous_page_url = fetch_and_save_recipe(
            search_query)

        context = {
            'results': search_results,
            'search_query': search_query,
            'current_page': current_page_url,
            'next_page': next_page_url,
            'previous_page': previous_page_url
        }

        return render(request, 'pages/results.html', context)

    return render(request, 'home.html')

# view function to get recipes from the previous page


def search_previous_results(request):
    if request.method == 'POST':
        next_page_url = request.POST.get('next_page_ulr')
        previous_page_url = request.POST.get('next_page_ulr')
        # FINISH VIEW FUNCTION WITH PREVIOUS PAGE LOGIC
        return None


# view function to get recipes in next page of response body
def search_next_recipes(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        next_page_url = request.POST.get('next_page_url')
        pre_previous_page = request.POST.get('previous_page_url')
        current_page_url = request.POST.get('current_page_url')

        if next_page_url:
            next_page_results, next_page, current_page, previous_page = fetch_and_save_next_page(
                next_page_url, current_page_url)

        return render(request, 'pages/results.html', {'results': next_page_results, 'search_query': search_query, 'next_page': next_page, 'current_page': current_page, 'previous_page': previous_page})

    return render(request, 'pages/results.html', {'results': None, 'search_query': '', 'next_page': None})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe
    }
    return render(request, 'pages/detail.html', context)


@login_required
def account_info_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'pages/account_info.html', context)

# def edit_account(request):
    user = request.user

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Redirect to the account info page after saving changes
            return redirect('account_info')
    else:
        form = EditAccountForm(instance=user)

    return render(request, 'pages/edit_account.html', {'form': form})
