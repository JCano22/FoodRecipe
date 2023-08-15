from django.urls import path
from .views import HomePageView, search_recipes, recipe_detail, search_next_recipes, search_previous_results
from . import views


urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("results/", search_recipes, name='results'),
    path("results/previous/", search_previous_results, name='previous_results'),
    path("results/next/", search_next_recipes, name='next_results'),
    path("results/<int:recipe_id>/", recipe_detail, name='details'),
    path("account_info/", views.account_info_view, name='account_info'),
    # path('edit-account/', views.edit_account, name='edit_account'),
]
