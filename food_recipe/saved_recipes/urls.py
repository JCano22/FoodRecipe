from django.urls import path
from .views import SavedRecipeListView, SaveRecipeView


urlpatterns = [
    path('list/', SavedRecipeListView.as_view(), name='saved_recipe_list'),
    path('save/<int:recipe_id>/', SaveRecipeView.as_view(), name='save_recipe'),
]
