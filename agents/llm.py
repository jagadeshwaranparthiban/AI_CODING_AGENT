from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text

def ask_json(prompt: str):

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    print(response.text)
    text = response.text.strip()

    try:
        return json.loads(text)

    except Exception:

        print("INVALID JSON:")
        print(text)

        raise