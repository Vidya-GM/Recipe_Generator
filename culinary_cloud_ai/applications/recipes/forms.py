from django import forms
from applications.recipes.models import CookingTime, Cuisine, Recipe, CheckboxIngredient


DIFFICULTY_CHOICES = Recipe.DIFFICULTY_CHOICES


class RecipeInputForm(forms.Form):

    ingredients = forms.ModelMultipleChoiceField(
        queryset=CheckboxIngredient.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,  # Or SelectMultiple
        label="Select Ingredients",
    )

    manual_ingredients = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False,
        label="Or enter ingredients manually"
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