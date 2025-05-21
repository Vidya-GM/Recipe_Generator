from django.contrib import admin
from applications.recipes.models import Recipe, CookingTime, Cuisine, CheckboxIngredient

# Register your models here.

admin.site.register(Recipe)
admin.site.register(CookingTime)
admin.site.register(Cuisine)
admin.site.register(CheckboxIngredient)
