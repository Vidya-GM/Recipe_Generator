from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import requests
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Manually define BASE_DIR and MEDIA_ROOT to match Django settings
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"


def generate_recipe_image(prompt: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return response.data[0].url


def download_image_to_media(url: str, filename: str) -> str:
    subfolder = "recipes_pic"
    media_dir = MEDIA_ROOT / subfolder
    media_dir.mkdir(parents=True, exist_ok=True)

    full_path = media_dir / f"{filename}.png"
    response = requests.get(url)

    if response.status_code == 200:
        with open(full_path, "wb") as f:
            f.write(response.content)
        print("Saved to:", full_path)
        return f"{MEDIA_URL}{subfolder}/{filename}.png"  # for DB or frontend
    else:
        raise Exception("Failed to download image.")


# # Example usage
# image_prompt = "A freshly made vegetarian salad with avocado and tomato in a white ceramic bowl, soft natural lighting"
# image_url = generate_recipe_image(image_prompt)
# print("Generated image URL:", image_url)

# local_media_path = download_image_to_media(image_url, "avocado_salad")
# print("Local media path (store in DB):", local_media_path)
