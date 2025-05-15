from django.urls import path
from applications.recipes.views.image_generator_views import simple_func

urlpatterns = [
    path("recipes/", simple_func, name="recipes"),
#     path('admin/', admin.site.urls),
#     path("", include("applications.recipe_user.urls")),
#     path("", include("applications.recipes.urls")),

]