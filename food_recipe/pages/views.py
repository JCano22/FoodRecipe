from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from recipes.views import fetch_and_save_recipe
from recipes.models import Recipe
from saved_recipes.models import SavedRecipe
import requests
import random
from django.contrib.auth.decorators import login_required
# from .forms import EditAccountForm


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

@login_required
def account_info_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'pages/account_info.html', context)

#def edit_account(request):
    user = request.user

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account_info')  # Redirect to the account info page after saving changes
    else:
        form = EditAccountForm(instance=user)

    return render(request, 'pages/edit_account.html', {'form': form})
