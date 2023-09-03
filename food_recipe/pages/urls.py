from django.urls import path
from .views import HomePageView, search_recipes, recipe_detail, search_filter
from . import views


urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("results/", search_recipes, name='results'),
    path("results/<int:recipe_id>/", recipe_detail, name='details'),
    path("filtered/", search_filter, name='filter'),
]
