# applications/recipes/urls.py
from django.urls import path
from .views import (
    GenerateCombinedView,
    RecipeListView,
    RecipeDetailView,
    home
)

app_name = 'recipes'
urlpatterns = [
    path('generate/', GenerateCombinedView.as_view(), name='generate_combined'),
    path('', home, name="home"),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipes/", RecipeListView.as_view(), name="recipe-list"),
]
