from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Cuisine(models.Model):
    cusine_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.cusine_name
    
class CookingTime(models.Model):
    time_in_minutes = models.PositiveIntegerField(help_text="Time is in minutes", unique=True)

    def __str__(self):
        return self.time_in_minutes


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    recipe_image = models.ImageField(upload_to='recipes_pic/',null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, blank=True)
    cooking_time = models.ForeignKey(CookingTime, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title