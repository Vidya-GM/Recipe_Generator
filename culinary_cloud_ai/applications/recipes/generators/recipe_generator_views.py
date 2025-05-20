from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_recipe_text(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-nano",  # or "gpt-4.0", "gpt-3.5-turbo", etc.
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )

    print("Usage stats:")
    print(f"  Prompt tokens: {response.usage.prompt_tokens}")
    print(f"  Completion tokens: {response.usage.completion_tokens}")
    print(f"  Total tokens: {response.usage.total_tokens}")

    return response.choices[0].message.content


# # Example usage
# result = generate_recipe_text("Create a vegetarian salad recipe with avocado and tomato")
# print(result)
