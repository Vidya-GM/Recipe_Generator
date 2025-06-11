from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class RecipeUser(AbstractUser):
    email = models.EmailField(max_length=100, blank=False, unique=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField(null=False, default=datetime.date(2005, 1, 1))
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profile_pic/', default="profile_pic/user-default.png")

    def __str__(self):
        return self.username


class Notification(models.Model):
    notif_recipient = models.ForeignKey(RecipeUser, on_delete=models.CASCADE, related_name="notifications")
    notif_message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic foreignkey to related object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["is_read", "-created_at"]

    def __str__(self):
        return f"To '{self.notif_recipient.username}': {self.notif_message[:50]}"
