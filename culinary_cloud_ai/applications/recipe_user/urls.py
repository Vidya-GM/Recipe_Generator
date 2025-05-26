from django.urls import path
from applications.recipe_user import views

urlpatterns = [

    path("login/", views.recipeuserLogin, name="login"),
    path("logout/", views.recipeuserLogout, name="logout"),
    path('register/', views.recipeuserRegister, name='register'),
    path("profile/", views.recipeuserDetails, name="profile"),
    path("update-profile/", views.recipeuserUpdate, name="update-profile"),

]

# http://127.0.0.1:8000/users/login/
# http://127.0.0.1:8000/users/logout/