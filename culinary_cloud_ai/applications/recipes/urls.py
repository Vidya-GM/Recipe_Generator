# applications/recipes/urls.py
from django.urls import path
from .views import (
    GenerateCombinedView,
    RecipeListView,
    RecipeDetailView,
    CommentDeleteView,
    toggle_like,
    home
)

app_name = 'recipes'

urlpatterns = [
    path('generate/', GenerateCombinedView.as_view(), name='generate_combined'),
    path('', home, name="home"),
    path("recipes/", RecipeListView.as_view(), name="recipe-list"),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path('toggle_like/<int:recipe_id>/', toggle_like, name='toggle_like'),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
    path('search/', RecipeListView.as_view(), name='search'),
]
