from django.contrib import admin
from applications.recipes.models import Recipe, CookingTime, Cuisine, CheckboxIngredient, Like, Comment


# Register your models here.

admin.site.register(Recipe)
admin.site.register(CookingTime)
admin.site.register(Cuisine)
admin.site.register(CheckboxIngredient)
admin.site.register(Like)
admin.site.register(Comment)