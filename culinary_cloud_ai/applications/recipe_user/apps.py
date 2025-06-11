from django.apps import AppConfig


class RecipeUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.recipe_user'

    def ready(self):
        import applications.recipe_user.signals