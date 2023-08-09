from django.urls import path
from .views import HomePageView, search_recipes, recipe_detail
from . import views

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("results/", search_recipes, name='results'),
    path("results/<int:recipe_id>/", recipe_detail, name='details'),
    path("account_info/", views.account_info_view, name='account_info'),
    #path('edit-account/', views.edit_account, name='edit_account'),
]
