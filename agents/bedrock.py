import boto3
import json
from typing import Type
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_ID = os.getenv("MODEL_ID")

client = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION")
)


def ask_gemini(prompt: str) -> str:
    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    )

    return response["output"]["message"]["content"][0]["text"]


def ask_json(prompt: str):

    prompt += """

    Return ONLY valid JSON.
    Do not wrap it in markdown.
    Do not use ```json.
    """

    response = ask_gemini(prompt)
    return json.loads(response)


def ask_structured(prompt: str, schema: Type[BaseModel]):

    prompt += f"""

    Return ONLY valid JSON matching this schema.

    DO NOT wrap the response in markdown.
    DO NOT use ```json.
    DO NOT explain anything.

    Schema:
    {json.dumps(schema.model_json_schema(), indent=2)}
    """

    response = ask_gemini(prompt)
    return schema.model_validate_json(response)