from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from .models import SavedRecipe
from recipes.models import Recipe

# Create your views here.


class SavedRecipeListView(LoginRequiredMixin, ListView):
    model = SavedRecipe
    template_name = 'saved_recipes/saved_list.html'
    context_object_name = 'saved_recipes'

    def get_queryset(self):
        return SavedRecipe.objects.filter(user=self.request.user)


class SaveRecipeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        recipe_id = kwargs['recipe_id']
        recipe = Recipe.objects.get(id=recipe_id)
        SavedRecipe.objects.create(user=request.user, recipe=recipe)
        return redirect('saved_recipe_list')
