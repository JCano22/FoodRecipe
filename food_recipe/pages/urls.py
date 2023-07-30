from django.urls import path
from .views import HomePageView, search_recipes, recipe_detail

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("results/", search_recipes, name='results'),
    path("results/<int:recipe_id>/", recipe_detail, name='details'),

]
