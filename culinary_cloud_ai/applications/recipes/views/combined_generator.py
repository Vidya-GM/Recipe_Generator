from recipe_generator_views import generate_recipe_text
from image_generator_views import generate_recipe_image, download_image_to_media
import re


def generate_full_recipe(prompt: str) -> dict:
    # 1. Generate the recipe text
    recipe_text = generate_recipe_text(prompt)

    # 2. Extract title from the recipe
    lines = recipe_text.splitlines()
    title_line = next(
        (line for line in lines if "title:" in line.lower() or "dish name:" in line.lower()),
        None
    )

    if title_line:
        raw_title = title_line.split(":", 1)[1].strip()
    elif lines and len(lines[0].strip()) > 3:
        raw_title = lines[0].strip()
    else:
        raw_title = "Unnamed Dish"

    # 3. Create safe filename from title
    filename = re.sub(r'[^a-zA-Z0-9_]', '', raw_title.lower().replace(" ", "_"))

    # 4. Generate image prompt using the dish name
    image_prompt = (
        f"A realistic photo of {raw_title}, use only ingredients from title, freshly cooked, served on a white ceramic plate, no any text on the image, "
        "natural lighting, visually appealing"
    )

    # 5. Generate the image
    image_url = generate_recipe_image(image_prompt)

    # 6. Download image to media/recipes_pic/
    local_image_path = download_image_to_media(image_url, filename)

    # 7. Return structured output
    return {
        "title": raw_title,
        "recipe_text": recipe_text,
        "image_url": image_url,
        "local_image_path": local_image_path
    }


if __name__ == "__main__":
    prompt = (
        "Use up to 400 tokens."
        "Create a recipe using the following ingredients: potato, chicken wings, honey, mustard."
        "Cooking time: up to 60 minutes."
        "Specifications (e.g., vegetarian, gluten-free): None."
        "Preparing type (fried, steamed, etc): Baked."
        "User preferences: None."
        "Start the recipe with this exact format:"
        "Title: <Dish Name>"
        "Then include the Ingredients list and Instructions."
    )

    data = generate_full_recipe(prompt)

    print("\n=== RECIPE GENERATED ===")
    print("\nTitle:", data["title"])
    print("\nImage URL:", data["image_url"])
    print("\nSaved to:", data["local_image_path"])
    print("\nFull Recipe:\n", data["recipe_text"])
