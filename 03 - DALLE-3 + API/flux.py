import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

system_prompt = "Generate an image of the iconic scene from the Titanic movie where Jack and Rose are standing at the bow of the ship, arms outstretched, embracing the feeling of freedom and love as they face the open ocean together."

request = requests.post(
    'https://api.bfl.ml/v1/flux-pro-1.1',
    headers={
        'accept': 'application/json',
        'x-key': os.getenv("FLUX_API_KEY"),
        'Content-Type': 'application/json'
    },
    json={
        'prompt': system_prompt,
        'width': 1440,  # Because max with is 1440 in Flux
        'height': 1024,
    }
).json()

request_id = request['id']

while True:
    time.sleep(0.5)
    result = requests.get(
        'https://api.bfl.ml/v1/get_result',
        headers={
            'accept': 'application/json',
            'x-key': os.environ.get("BFL_API_KEY"),
        },
        params={
            'id': request_id,
        },
    ).json()
    if result["status"] == "Ready":
        # Download image from url and create a flux-image.jpg file
        image = requests.get(result['result']['sample'])
        with open("flux-images/flux-image.jpg", "wb") as file:
            file.write(image.content)
        break
