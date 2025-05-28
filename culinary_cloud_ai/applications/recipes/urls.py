# applications/recipes/urls.py
from django.urls import path
from .views import (
    GenerateCombinedView,
    RecipeListView,
    RecipeDetailView,
    toggle_like
)

app_name = 'recipes'
urlpatterns = [
    path('generate/', GenerateCombinedView.as_view(), name='generate_combined'),
    path('', RecipeListView.as_view(), name="home"),
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path('toggle_like/<int:recipe_id>/', toggle_like, name='toggle_like'),
]
