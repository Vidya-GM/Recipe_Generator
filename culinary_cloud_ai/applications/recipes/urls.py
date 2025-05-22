# applications/recipes/urls.py
from django.urls import path
from .views import (
    GenerateCombinedView,
)

app_name = 'recipes'
urlpatterns = [
    # Combined generation endpoint
    path('generate/', GenerateCombinedView.as_view(), name='generate_combined'),
]
