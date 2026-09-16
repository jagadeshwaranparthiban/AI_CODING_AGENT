from typing import Type
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os
from .logger import logger
from .exceptions import LLMError

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    raise LLMError("GEMINI_API_KEY is not set in the environment variables.")

client = genai.Client(api_key=api_key)

def ask_gemini(prompt: str):
    try:
        response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
        
        if not response.text:
            raise LLMError("Empty response from Gemini API.")
            
        return response.text
    
    except LLMError:
        raise

    except Exception as e:
        logger.exception("Gemini request failed")

        raise LLMError(
            "Failed to generate response from Gemini."
        ) from e
    


def ask_structured(prompt: str, schema: Type[BaseModel]):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema
            }
        )

        if not response.text:
            raise LLMError("Empty response from Gemini API.")
        return schema.model_validate_json(response.text)

    except LLMError:
        raise

    except Exception as e:
        logger.exception("Gemini request failed")

        raise LLMError(
            "Failed to generate structured response from Gemini."
        ) from e

