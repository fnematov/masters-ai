import os
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

# Create an instance of the OpenAI class
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
As a senior Copywriter, you have tasked to write blog post based on lesson transcript about AI and ML overview.

Requirements for blog post:
1. Be creative. Generate unique and creative text
2. Blog post should be with title.
3. Try to cover all important points.
4. Divide blog post with headlines
5. Generate images for cover and main headlines
6. Mark important points with bold or underlined text
7. Provide result on .md file syntax.
8. Not mark result as code block. Use markdown syntax. Because it will be used in README.md file.
"""

# Read file content from transcript.txt file
with open("transcript.txt", "r") as file:
    transcript = file.read()

result = openai.chat.completions.create(
    model="gpt-4o",
    temperature=0.7,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": transcript},
    ]
)

with open("README.md", "w") as file:
    file.write(result.choices[0].message.content)