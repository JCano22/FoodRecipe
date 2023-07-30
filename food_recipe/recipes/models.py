from django.db import models

# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.URLField()
    image_url = models.URLField()
    calories = models.DecimalField(max_digits=6, decimal_places=2)
    cuisine = models.TextField()

    def __str__(self):
        return self.title
