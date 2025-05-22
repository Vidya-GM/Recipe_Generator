# applications/recipes/urls.py
from django.urls import path
from .views import (
    GenerateCombinedView,
    home

)

app_name = 'recipes'
urlpatterns = [
    path('generate/', GenerateCombinedView.as_view(), name='generate_combined'),
    path('', home, name="home"),
]
