import boto3
import json
from typing import Type
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from .logger import logger
from .exceptions import LLMError, ToolNotFoundError
from .bedrock_tools import TOOLS, execute_tool

load_dotenv()

MODEL_ID = os.getenv("MODEL_ID")
AWS_REGION = os.getenv("AWS_REGION")

if not MODEL_ID:
    raise LLMError("MODEL_ID is not set in the environment variables.")
if not AWS_REGION:
    raise LLMError("AWS_REGION is not set in the environment variables.")

client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION
)


def ask_gemini(prompt: str) -> str:
    try:
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
        if not response or "output" not in response or "message" not in response["output"]:
            raise LLMError("Invalid response from Gemini API.")
        
        return response["output"]["message"]["content"][0]["text"]
    except LLMError:
        raise

    except Exception as e:
        logger.exception("Gemini request failed")
        raise LLMError(
            "Failed to generate response from Gemini."
        ) from e


def ask_structured(prompt: str, schema: Type[BaseModel]):

    prompt += f"""

    Return ONLY valid JSON matching this schema.

    DO NOT wrap the response in markdown.
    DO NOT use ```json.
    DO NOT explain anything.

    Schema:
    {json.dumps(schema.model_json_schema(), indent=2)}
    """

    try:
        response = ask_gemini(prompt)

        if not response:
            raise LLMError("Empty response from Gemini API.")
        
        return schema.model_validate_json(response)
    except LLMError:
        raise
    except Exception as e:
        logger.exception("Failed to validate structured response")
        raise LLMError("Failed to generate structured response.") from e


def ask_with_tools(prompt: str,max_iterations: int = 10):

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": prompt
                }
            ]
        }
    ]

    for iteration in range(max_iterations):

        response = client.converse(
            modelId=MODEL_ID,
            messages=messages,
            toolConfig={
                "tools": TOOLS
            }
        )

        output_message = response["output"]["message"]
        messages.append(output_message)
        stop_reason = response["stopReason"]

        if stop_reason == "end_turn":
            text_parts = [
                block["text"]
                for block in output_message.get("content", [])
                if "text" in block
            ]

            return "\n".join(text_parts)

        if stop_reason == "tool_use":
            tool_results = []

            for content_block in output_message["content"]:

                if "toolUse" not in content_block:
                    continue

                tool_use = content_block["toolUse"]

                tool_name = tool_use["name"]
                tool_use_id = tool_use["toolUseId"]
                tool_input = tool_use["input"]

                print(f"Tool requested: {tool_name}")
                print(f"Tool input: {tool_input}")

                try:
                    result = execute_tool(
                        tool_name,
                        tool_input
                    )

                    tool_result = {
                        "toolUseId": tool_use_id,
                        "content": [
                            {
                                "json": {
                                    "result": result
                                }
                            }
                        ]
                    }

                except ToolNotFoundError as e:
                    tool_result = {
                        "toolUseId": tool_use_id,
                        "content": [
                            {
                                "json": {
                                    "error": str(e)
                                }
                            }
                        ]
                    }
                except Exception as e:

                    tool_result = {
                        "toolUseId": tool_use_id,
                        "content": [
                            {
                                "json": {
                                    "error": str(e)
                                }
                            }
                        ]
                    }

                tool_results.append(
                    {
                        "toolResult": tool_result
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": tool_results
                }
            )

            continue

        raise RuntimeError(
            f"Unexpected Bedrock stop reason: {stop_reason}"
        )

    raise RuntimeError(
        f"Tool-calling loop exceeded "
        f"{max_iterations} iterations."
    )