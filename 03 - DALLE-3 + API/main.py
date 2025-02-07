import os
from dotenv import load_dotenv
import requests
from openai import OpenAI

load_dotenv()

# Create an instance of the OpenAI class
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the base prompt for the image generation
base_prompt = (
    "Generate an image of the iconic scene from the Titanic movie where Jack and Rose "
    "are standing at the bow of the ship, arms outstretched, embracing the feeling of freedom "
    "and love as they face the open ocean together"
)

# Pre-defined list of different artistic styles
styles = [
    "vintage",
    "modern",
    "abstract",
    "impressionist",
    "pop art",
    "watercolor",
    "digital painting",
    "line art",
    "minimalist"
]

# Create a directory to save the images if it doesn't exist
output_dir = "openai-images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop over each style and generate an image with the style appended to the prompt
for style in styles:
    # Combine the base prompt with the current style
    styled_prompt = f"{base_prompt} in a {style} style."
    print(f"Generating image with prompt: {styled_prompt}")

    result = openai.images.generate(
        model="dall-e-3",
        prompt=styled_prompt,
        size="1024x1024",
        quality="hd",
        n=1,  # Generate one image per style
    )

    # Get the image URL from the result
    image_url = result.data[0].url

    # Download the image and save it to a file named after the style
    image = requests.get(image_url)
    image_path = os.path.join(output_dir, f"titanic_{style}.jpg")
    with open(image_path, "wb") as file:
        file.write(image.content)

    print(f"Image saved for style '{style}' at {image_path}")