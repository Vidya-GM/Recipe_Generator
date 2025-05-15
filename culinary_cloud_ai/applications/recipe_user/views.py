from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def simple_func(request):
    return HttpResponse("from recipe_users")