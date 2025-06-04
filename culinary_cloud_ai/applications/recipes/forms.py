from django import forms
from applications.recipes.models import CookingTime, Cuisine, Recipe, CheckboxIngredient, Comment


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
        label="Ingredients or preferences"
    )

    difficulty = forms.ChoiceField(
        choices=Recipe.DIFFICULTY_CHOICES,
        required=True,
        initial="Medium",
        label="Difficulty",
    
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


class RecipeCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,        # height
                'cols': 75,       # width
                'placeholder': 'Write a comment...',
            }),
        }