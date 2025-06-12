from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from applications.recipes.models import Recipe, Comment, Like
from applications.recipe_user.models import Notification, RecipeUser


@receiver(post_save, sender=Comment)
def notify_on_new_comment(sender, instance, created, **kwargs):
    if created and instance.recipe.recipe_owner != instance.author:
        Notification.objects.create(
            notif_recipient=instance.recipe.recipe_owner,
            notif_message=f"{instance.author.username} commented on '{instance.recipe}'",
            content_type=ContentType.objects.get_for_model(Comment),
            object_id=instance.id,
        )
        print("Ok")

@receiver(post_save, sender=Like)
def notify_on_like(sender, instance, created, **kwargs):
    if created and instance.recipe.recipe_owner != instance.author:
        Notification.objects.create(
            notif_recipient=instance.recipe.recipe_owner,
            notif_message=f"{instance.author.username} liked your {instance.recipe}",
            content_type=ContentType.objects.get_for_model(Like),
            object_id=instance.id,
        )

# @receiver(post_save, sender=Recipe)
# def notify_on_new_recipe(sender, instance, created, **kwargs):
#     if created:
#         users_to_notify = RecipeUser.objects.exclude(id=instance.recipe_owner.id)

#         for user in users_to_notify:
#             Notification.objects.create(
#                 notif_recipient=user,
#                 notif_message=f"{instance.recipe_owner} added a new recipe {instance.title}",
#                 content_type=ContentType.objects.get_for_model(Recipe),
#                 object_id=instance.id,
#             ) 