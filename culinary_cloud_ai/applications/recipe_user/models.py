from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

#Create your models here.

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