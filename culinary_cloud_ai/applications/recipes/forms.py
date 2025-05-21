from django import forms
from applications.recipes.models import CookingTime, Cuisine, Recipe, Ingredients


DIFFICULTY_CHOICES = Recipe.DIFFICULTY_CHOICES


class RecipeInputForm(forms.Form):

    instructions = forms.ModelMultipleChoiceField(
        queryset=Ingredients.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,  # Or SelectMultiple
        label="Select Ingredients",
    )

    difficulty = forms.ChoiceField(
        choices=Recipe.DIFFICULTY_CHOICES,
        required=True,
        initial="Medium",
        label="Choose a difficulty",
    
    )

    cuisine = forms.ModelChoiceField(
        queryset=Cuisine.objects.all(),
        required=False,
        label="Cuisine",
        empty_label="Choose a cuisine",
    )

    cooking_time = forms.ModelChoiceField(
        queryset=CookingTime.objects.all(),
        required=False,
        label="Cooking Time",
        empty_label="Select cooking time",
    )