from django.urls import path
from applications.recipe_user import views

urlpatterns = [

    path("login/", views.recipeuserLogin, name="login"),
    path("logout/", views.recipeuserLogout, name="logout"),
    path('register/', views.recipeuserRegister, name='register'),
    path("profile/", views.recipeuserDetails, name="profile"),
    path("update-profile/", views.recipeuserUpdate, name="update-profile"),
    path("my-recipes/", views.myRecipes, name="my-recipes"),
    path("notifications/", views.notificationList, name="notification-list"),
    path("notifications/visit/<int:pk>/", views.notificationVisit, name="notification-visit"),
    path('notifications/delete-selected/', views.delete_selected_notification, name='delete-selected-notifications'),

]

# http://127.0.0.1:8000/users/login/
# http://127.0.0.1:8000/users/logout/