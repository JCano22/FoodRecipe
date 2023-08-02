from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe

# Create your models here.


class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"
