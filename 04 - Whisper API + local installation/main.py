import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from a .env file
load_dotenv()

# Create an instance of the OpenAI class using your API key
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Open the audio file in binary mode
with open("recording.mp3", "rb") as audio_file:
    # Generate the transcription using OpenAI's Whisper model
    response = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )

# Extract the transcription text from the response
transcription_text = response.text

# Print the transcribed text
print("Transcription:", transcription_text)

# Write the transcription to a file
with open("transcription.txt", "w") as output_file:
    output_file.write(transcription_text)