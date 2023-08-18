from django.urls import path
from .views import SaveRecipeView

urlpatterns = [
    path('', SaveRecipeView.as_view, name='save_recipe'),
]
