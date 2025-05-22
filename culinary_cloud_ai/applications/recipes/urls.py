from django.urls import path
from applications.recipes import views
from django.contrib import admin
from django.urls import include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("applications.recipe_user.urls")),
    path("", views.home, name="index"),
    path("recipe/", views.recipe_placeholder, name="recipe_placeholder"),

]