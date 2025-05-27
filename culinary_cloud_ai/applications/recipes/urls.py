# applications/recipes/urls.py
from django.urls import path
from .views import (
    GenerateCombinedView,
    RecipeListView

)

app_name = 'recipes'
urlpatterns = [
    path('generate/', GenerateCombinedView.as_view(), name='generate_combined'),
    path('', RecipeListView.as_view(), name="home"),
]
