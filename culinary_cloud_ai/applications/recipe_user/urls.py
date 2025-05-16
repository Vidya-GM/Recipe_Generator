from django.urls import path
from applications.recipe_user import views

urlpatterns = [

    path("login/", views.simple_func, name="recipe_user"),


]

# http://127.0.0.1:8000/users/login/
# http://127.0.0.1:8000/users/logout/