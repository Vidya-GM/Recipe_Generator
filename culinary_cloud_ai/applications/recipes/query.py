from .models import Recipe, Cuisine, CookingTime
from typing import Dict, Optional
from django.conf import settings
import os
from django.core.files import File

def save_generated_recipe(data: Dict, user=None) -> Recipe:
    """
    Save the generated recipe data to the database.
    
    Args:
        data (dict): The dictionary returned from the AI generation function.

    Returns:
        Recipe: The saved Recipe instance.
    """

    # Process cooking time
    cooking_minutes_raw = data.get("cooking_time", "0")
    cooking_minutes = ''.join(filter(str.isdigit, cooking_minutes_raw))
    cooking_minutes = int(cooking_minutes) if cooking_minutes.isdigit() else None

    time_obj = None
    if cooking_minutes:
        time_obj, _ = CookingTime.objects.get_or_create(time_in_minutes=cooking_minutes)

    # Process cuisine
    cuisine_name = data.get('cuisine', 'Unknown')
    cuisine_obj, _ = Cuisine.objects.get_or_create(cuisine_name=cuisine_name)

    # Convert ingredients and instructions from list to plain text
    ingredients_text = "\n".join(data.get('ingredients', []))
    instructions_text = "\n".join(data.get('instructions', []))

    # Save the Recipe
    recipe = Recipe.objects.create(
        title=data.get('title', ''),
        description=data.get('description', ''),
        ingredients=ingredients_text,
        instructions=instructions_text,
        difficulty=data.get('difficulty', 'Medium'),
        cuisine=cuisine_obj,
        cooking_time=time_obj,
        #recipe_image=None,
        recipe_owner=user if getattr(user, "is_authenticated", False) else None
    )    

    image_path = data.get('local_image_path')

    if image_path:
        media_url = settings.MEDIA_URL  # in base.py it is '/media/'
        if image_path.startswith(media_url):
            image_path = os.path.join(settings.MEDIA_ROOT, image_path[len(media_url):])
        elif not os.path.isabs(image_path):
            image_path = os.path.join(settings.MEDIA_ROOT, image_path.lstrip('/'))

        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                recipe.recipe_image.save(os.path.basename(image_path), File(f), save=True)
    else:
        pass  # no image path, nothing to do

    return recipe