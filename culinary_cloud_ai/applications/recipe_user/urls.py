from django.urls import path
from applications.recipe_user import views

urlpatterns = [

    path("recipe_user", views.simple_func, name="recipe_user"),


]