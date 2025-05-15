from django.db import models
from django.conf import settings


class Recipe(models.Model):
    # link to the user who generated it
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes"
    )

    # basic fields
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # optional short summary
    ingredients = models.TextField()
    instructions = models.TextField()

    # image: store URL from OpenAI or uploaded later
    image_url = models.URLField(blank=True, null=True)

    # metadata
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")
    difficulty = models.CharField(
        max_length=50,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ]
    )

    # tags, categories, etc. can be added later
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
