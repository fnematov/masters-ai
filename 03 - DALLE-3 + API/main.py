import os
from dotenv import load_dotenv
import requests
from openai import OpenAI

load_dotenv()


# Create an instance of the OpenAI class
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = "Generate an image of the iconic scene from the Titanic movie where Jack and Rose are standing at the bow of the ship, arms outstretched, embracing the feeling of freedom and love as they face the open ocean together."

result = openai.images.generate(
    model="dall-e-3",
    prompt=system_prompt,
    size="1792x1024",
    quality="hd",
    n=1,
)

image_url = result.data[0].url

# Download image from url and create an image.jpg file
image = requests.get(image_url)
with open("image.jpg", "wb") as file:
    file.write(image.content)