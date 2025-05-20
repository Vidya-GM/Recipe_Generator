        prompt = f"""
You are an AI chef assistant. Generate a complete, structured recipe based on the following constraints.
Use up to 500 tokens.

Respond in **two parts**:

---

PART 1 — Human-readable recipe (for user display):

- Title: <Dish Name>
- Short Description: <1–2 sentence summary>
- Ingredients:
- item 1
- item 2
- Instructions:
1. Step one
2. Step two

---

PART 2 — Structured data in JSON format:
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