from .recipe_generator_views import generate_recipe_text
from .image_generator_views import generate_recipe_image, download_image_to_media
import json
import re
import uuid


def generate_full_recipe(prompt: str) -> dict:
    # 1. Generate the recipe text from GPT
    full_response = generate_recipe_text(prompt)

    # 2. Extract JSON block from the full response
    json_part = None
    if "```json" in full_response:
        json_start = full_response.find("```json") + len("```json")
        json_end = full_response.find("```", json_start)
        json_part = full_response[json_start:json_end].strip()
    else:
        json_start = full_response.find("{")
        json_part = full_response[json_start:].strip()

    try:
        structured = json.loads(json_part)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON from GPT response.")
        print("Error:", e)
        print("Raw response was:\n", full_response)
        return {}

    # 3. Generate a safe filename from the recipe title
    raw_title = structured.get("title", "Unnamed Dish")
    filename = re.sub(r'\W+', '_', raw_title.lower()).strip('_')

    # 3.1 Append a short unique ID so names never collide
    unique_id = uuid.uuid4().hex[:8]
    filename_with_uuid = f"{filename}_{unique_id}"

    # 4. Generate image prompt using the dish description
    description = structured.get("description", raw_title)
    image_prompt = (
        f"A highly realistic photo of a freshly cooked dish featuring {description}, made exclusively using the ingredients mentioned."
        "The dish is elegantly plated on a clean white ceramic plate, styled to highlight its freshness and appeal."
        "Captured in soft, natural lighting, with no text or labels, and composed for maximum visual allure and gourmet presentation."
        "WITHOUT any text on the image"
    )

    # 5. Generate and download the image
    image_url = generate_recipe_image(image_prompt)
    local_image_path = download_image_to_media(image_url, filename_with_uuid)

    # 6. Return everything structured
    return {
        "title": structured.get("title"),
        "description": structured.get("description"),
        "ingredients": structured.get("ingredients", []),
        "instructions": structured.get("instructions", []),
        "difficulty": structured.get("difficulty"),
        "cuisine": structured.get("cuisine"),
        "cooking_time": structured.get("cooking_time"),
        "image_url": image_url,
        "local_image_path": local_image_path,
        # "raw_response": full_response  # optional for debugging
    }


# if __name__ == "__main__":
    # prompt = """
    # You are an AI chef assistant. Generate a complete, structured recipe based on the following constraints.
    # Use up to 500 tokens.

    # Respond in **two parts**:

    # ---

    # PART 1 — Human-readable recipe (for user display):

    # - Title: <Dish Name>
    # - Short Description: <1–2 sentence summary>
    # - Ingredients:
    # - item 1
    # - item 2
    # - Instructions:
    # 1. Step one
    # 2. Step two

    # ---

    # PART 2 — Structured data in JSON format:
    # Return a JSON object with the following fields:

    # {
    #   "title": "<Dish Name>",
    #   "description": "<Short Description>",
    #   "ingredients": ["<ingredient1>", "<ingredient2>", "..."],
    #   "instructions": ["<step1>", "<step2>", "..."],
    #   "difficulty": "<Easy|Medium|Hard>",
    #   "cuisine": "<Cuisine Name>",
    #   "cooking_time": "<Time in minutes, e.g. '30'>"
    # }

    # ---

    # Constraints:
    # - Use only these difficulty values: Easy, Medium, Hard
    # - Cuisine and cooking_time should be realistic but made up if needed
    # - Do NOT include image, calories, or preparation time separately
    # - Ensure JSON is valid and follows the key naming exactly
    # - Return raw JSON only, do not wrap it in triple backticks or markdown

    # ---

    # Generate a recipe using the following ingredients: salmon filet, lime, honey.
    # Cooking time: under 60 minutes.
    # Type: Any.
    # Serving suggestion: simple but elegant dish.
    # """

    # data = generate_full_recipe(prompt)
    # # Debugging prints
    # if data:
    #     print("\n=== RECIPE GENERATED ===")
    #     print("Title:", data["title"])
    #     print("Description:", data["description"])

    #     print("\nIngredients:")
    #     for ing in data["ingredients"]:
    #         print("-", ing)

    #     print("\nInstructions:")
    #     for i, step in enumerate(data["instructions"], start=1):
    #         print(f"{i}. {step}")

    #     print("\nDifficulty:", data["difficulty"])
    #     print("Cuisine:", data["cuisine"])
    #     print("Cooking Time:", data["cooking_time"])

    #     print("\nImage URL:", data["image_url"])
    #     print("Saved to:", data["local_image_path"])

        # # Print full response for debugging
        # print("\n=== FULL RESPONSE ===")
        # print(data["raw_response"])
