# Create your models here.
from django.db import models
from django.urls import reverse


class CheckboxIngredient(models.Model):
    CATEGORY_MEAT = "MEAT"
    CATEGORY_VEG = "VEG"
    CATEGORY_FRUIT = "FRUIT"
    CATEGORY_DAIRY = "DAIRY"
    CATEGORY_OTHER = "OTHER"

    CATEGORY_CHOICES = [
        (CATEGORY_MEAT,  "Meat"),
        (CATEGORY_VEG,   "Veggies"),
        (CATEGORY_FRUIT, "Fruits"),
        (CATEGORY_DAIRY, "Dairy"),
        (CATEGORY_OTHER, "Other"),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_OTHER,
        help_text="Select the category for this ingredient.",
    )

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        display = dict(self.CATEGORY_CHOICES).get(self.category, self.category)
        return f"{self.name} ({display})"


class Cuisine(models.Model):
    cuisine_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.cuisine_name


class CookingTime(models.Model):
    time_in_minutes = models.PositiveIntegerField(help_text="Time is in minutes", unique=True)

    class Meta:
        # Always return CookingTime objects in ascending order by time_in_minutes
        ordering = ["time_in_minutes"]

    def __str__(self):
        return f"{self.time_in_minutes} minutes"


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    recipe_owner = models.ForeignKey("recipe_user.RecipeUser", null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    recipe_image = models.ImageField(upload_to='recipes_pic/', null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, blank=True, related_name="recipes")
    cooking_time = models.ForeignKey(CookingTime, on_delete=models.SET_NULL, null=True, blank=True, related_name="recipes")
    created_at = models.DateTimeField(auto_now_add=True)

    # Returns the absolute URL for the recipe detail view
    def get_absolute_url(self):
        return reverse("recipes:recipe-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def liked_users(self):
        return [like.author for like in self.likes.select_related('user')]

    @property
    def comments_count(self):
        return self.comments.count()


class Like(models.Model):
    author = models.ForeignKey("recipe_user.RecipeUser", on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'recipe')  # Prevents duplicate likes

    def __str__(self):
        return f"{self.author.username} liked {self.recipe}"


class Comment(models.Model):
    author = models.ForeignKey("recipe_user.RecipeUser", on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.recipe.title}"

    class Meta:
        ordering = ['-created_at']
