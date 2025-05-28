from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .forms import RecipeInputForm
from .generators.combined_generator import generate_full_recipe
from .query import save_generated_recipe

from django.views.generic import ListView, DetailView
from .models import Recipe, Like
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count, Exists, OuterRef, Q

def home(request):
    return render(request, "recipes/home.html")

def home(request):
    return render(request, "recipes/home.html")

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(likes_count=Count('likes'))
        user = self.request.user
        if user.is_authenticated:
            user_likes = Like.objects.filter(author=user, recipe=OuterRef('pk'))
            queryset = queryset.annotate(user_liked=Exists(user_likes))
        else:
            queryset = queryset.annotate(user_liked=Q(pk__isnull=True))  # always False
        return queryset

@login_required
def toggle_like(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    
    like, created = Like.objects.get_or_create(author=user, recipe=recipe)
    if not created:
        # User already liked this recipe, so unlike it
        like.delete()

    return redirect('recipes:recipe-detail', pk=recipe.id)

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context["user_has_liked"] = False
        if self.request.user.is_authenticated:
            context["user_has_liked"] = recipe.likes.filter(author=self.request.user).exists()
        return context


class GenerateCombinedView(View):
    """Run the full pipeline (text + image) and then redirect to the saved recipe."""

    def get(self, request):
        form = RecipeInputForm()
        return render(request, "recipes/generate_combined.html", {"form": form})

    def post(self, request):
        form = RecipeInputForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("Form is not valid.")

        # Gather form data
        selected_ingredients = form.cleaned_data["ingredients"]
        manual_ingredients = form.cleaned_data.get("manual_ingredients", "")
        cooking_time = form.cleaned_data.get("cooking_time")
        cuisine = form.cleaned_data.get("cuisine")
        difficulty = form.cleaned_data.get("difficulty")

        # Build ingredient string
        combined_ingredients = [ing.name for ing in selected_ingredients]
        if manual_ingredients:
            combined_ingredients.append(manual_ingredients)
        ingredients_str = ", ".join(combined_ingredients)

        cooking_time_str = (
            f"{cooking_time.time_in_minutes}" if cooking_time else "unspecified"
        )
        cuisine_str = cuisine.cuisine_name if cuisine else "unspecified"

        # Build the AI prompt
        prompt = f"""
You are an AI chef assistant. Generate a complete, structured recipe based on the following constraints.
Use up to 500 tokens.

Respond in **following format**:

Structured data in JSON format:

Return a JSON object with the following fields:

{{
  "title": "<Dish Name>",
  "description": "<Short Description>",
  "ingredients": ["<ingredient1>", "<ingredient2>", "..."],
  "instructions": ["<step1>", "<step2>", "..."],
  "difficulty": "<Easy|Medium|Hard>",
  "cuisine": "<Cuisine Name>",
  "cooking_time": "<Time in minutes, e.g. '30'>"
}}

---

Constraints:
- Use only these difficulty values: Easy, Medium, Hard
- Cuisine and cooking_time should be realistic but made up if needed
- Do NOT include image, calories, or preparation time separately
- Ensure JSON is valid and follows the key naming exactly
- Return raw JSON only, do not wrap it in triple backticks or markdown

---

Filter out any inappropriate, harmful, or non-edible ingredients
(e.g., gasoline, porn, wood, drugs). Only use safe, edible items.

---

Generate a recipe using the following ingredients: {ingredients_str}.
Cooking time: {cooking_time_str}.
Cuisine: {cuisine_str}.
Difficulty: {difficulty}.
"""

        try:
            result = generate_full_recipe(prompt)
            # save_generated_recipe should return the Recipe instance
            recipe = save_generated_recipe(result, user=request.user)
        except Exception as e:
            return HttpResponseBadRequest(f"AI generation error: {e}")

        # Redirect to the newly created recipe's detail page
        return redirect(recipe.get_absolute_url())
