from django.views import View
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .forms import RecipeInputForm
from .generators.combined_generator import generate_full_recipe


class GenerateCombinedView(View):
    """Run the full pipeline (text + image) and render a recipe page."""

    def get(self, request):
        form = RecipeInputForm()
        return render(request, 'recipes/generate_combined.html', {'form': form})

    def post(self, request):
        form = RecipeInputForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('Form is not valid.')

        # Extract checkbox ingredients (model instances)
        selected_ingredients = form.cleaned_data['ingredients']  # List of CheckboxIngredient instances
        manual_ingredients = form.cleaned_data.get('manual_ingredients', '')
        cooking_time = form.cleaned_data.get('cooking_time')
        cuisine = form.cleaned_data.get('cuisine')
        difficulty = form.cleaned_data.get('difficulty')

        # Convert ingredient objects to strings
        combined_ingredients = [ing.name for ing in selected_ingredients]
        if manual_ingredients:
            combined_ingredients.append(manual_ingredients)

        ingredients_str = ', '.join(combined_ingredients)
        cooking_time_str = f"{cooking_time.time_in_minutes}" if cooking_time else "unspecified"
        cuisine_str = cuisine.cuisine_name if cuisine else "unspecified"

        # Build the prompt
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
        except Exception as e:
            return HttpResponseBadRequest(f"AI generation error: {e}")

        return render(request, 'recipes/recipe_detail.html', {
            'title': result.get('title', ''),
            'description': result.get('description', ''),
            'ingredients': result.get('ingredients', []),
            'instructions': result.get('instructions', []),
            'difficulty': result.get('difficulty', ''),
            'cuisine': result.get('cuisine', ''),
            'cooking_time': result.get('cooking_time', ''),
            'image_url': result.get('image_url') or result.get('local_path'),
        })
