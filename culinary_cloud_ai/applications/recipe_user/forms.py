from django import forms
from django.contrib.auth.forms import UserCreationForm
from applications.recipe_user.models import RecipeUser


class RecipeUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)))

    class Meta:
        model = RecipeUser
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'date_of_birth', 'profile_image']


class RecipeUserUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, 2025))
    )

    class Meta:
        model = RecipeUser
        fields = ['username', 'email', 'bio', 'date_of_birth', 'profile_image']