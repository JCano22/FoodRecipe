from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from recipes.views import fetch_and_save_recipe
from recipes.models import Recipe


class HomePageView(TemplateView):
    template_name = "pages/home.html"


# view function to search api with keyword from user


def search_recipes(request):
    if request.method == 'POST':
        print(request.POST)
        search_query = request.POST.get('search_query', '')
        print("search_query:", search_query)
        # Recipe.objects.all().delete()

        search_results = fetch_and_save_recipe(search_query)
        return render(request, 'pages/results.html', {'results': search_results})
    return render(request, 'home.html')


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe
    }
    return render(request, 'pages/detail.html', context)
