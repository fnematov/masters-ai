import os
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

# Create an instance of the OpenAI class
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

audio_file = open("recording.mp3", "rb")

response = openai.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
)

# Print the transcribed text
print("Transcription:", response.text)