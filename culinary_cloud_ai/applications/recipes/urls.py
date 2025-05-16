from django.urls import path
from applications.recipes import views

urlpatterns = [
    path("", views.home, name="home"),

]
