# Building a recipe prompt for OpenAI API

def build_recipe_prompt(ingredients: list, preferences: str = "", cooking_time: int = 30, specs: str = "", preparing_type: str = "any") -> str:
    ingredients_text = ", ".join(ingredients)
    prompt = (
        f"Create a recipe using the following ingredients: {ingredients_text}.\n"
        f"Cooking time: up to {cooking_time} minutes.\n"
        f"Specifications (e.g., vegetarian, gluten-free): {specs or 'None'}.\n"
        f"Preparing type (fried, steamed, etc): {preparing_type}.\n"
        f"User preferences: {preferences or 'None'}.\n"
        f"Include title, ingredients list, and step-by-step instructions."
    )
    return prompt
