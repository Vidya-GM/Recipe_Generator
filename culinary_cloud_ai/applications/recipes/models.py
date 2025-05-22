# Create your models here.
from django.db import models

# Create your models here.


class CheckboxIngredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    cuisine_name = models.CharField(max_length=100, unique=True)
    cuisine_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.cuisine_name


class CookingTime(models.Model):
    time_in_minutes = models.PositiveIntegerField(help_text="Time is in minutes", unique=True)

    def __str__(self):
        return f"{self.time_in_minutes} minutes"
    
class CheckboxIngredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    recipe_owner = models.ForeignKey("recipe_user.RecipeUser", null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    recipe_image = models.ImageField(upload_to='recipes_pic/', null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, blank=True, related_name="recipes")
    cooking_time = models.ForeignKey(CookingTime, on_delete=models.SET_NULL, null=True, blank=True, related_name="recipes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
