from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    ingredients = ["Flour", "Eggs", "Milk", "Butter", "Sugar", "Salt"]
    return render(request, "recipes/home.html", {
        "ingredients": ingredients
        
    })

def recipe_placeholder(request):
    return render(request, "recipes/recipe.html")
