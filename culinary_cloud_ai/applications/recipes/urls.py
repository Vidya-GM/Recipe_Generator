from django.urls import path
from applications.recipes import views

urlpatterns = [
    
    path("recipes", views.simple_function, name="recipes"),

]
