from django.urls import path
from .views import HomePageView, search_recipes

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("results/", search_recipes, name='results')

]
