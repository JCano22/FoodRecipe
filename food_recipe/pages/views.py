from django.shortcuts import render
from django.views.generic import TemplateView
from recipes.views import fetch_and_save_recipe

# Create your views here.


class HomePageView(TemplateView):
    template_name = "pages/home.html"


# view function to search api with keyword from user


def search_recipes(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')

        search_results = fetch_and_save_recipe(search_query)

        return render(request, 'pages/results.html', {'results': search_results})
    return render(request, 'home.html')
