# applications/recipes/views.py
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest

from .generators.combined_generator import generate_full_recipe

class GenerateCombinedView(View):
    """Run the full pipeline (text + image) and return structured data."""
    def get(self, request):
        # Render a unified form for ingredients and options
        return render(request, 'generate_combined.html')

    def post(self, request):
        # Gather user inputs
        ingredients = request.POST.get('ingredients', '')
        cooking_time = request.POST.get('cooking_time', '')
        dish_type = request.POST.get('dish_type', '')
        serving_suggestion = request.POST.get('serving_suggestion', '')

        if not ingredients:
            return HttpResponseBadRequest('Missing `ingredients` field.')

        # Build the combined prompt
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

Generate a recipe using the following ingredients: {ingredients}.
Cooking time: {cooking_time}.
Type: {dish_type}.
Serving suggestion: {serving_suggestion}.
"""
        try:
            # Call the combined generator which returns both text and images
            result = generate_full_recipe(prompt)
            return JsonResponse(result, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))
