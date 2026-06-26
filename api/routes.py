from fastapi import APIRouter
from agents.graph import agent
from uuid import uuid4

router = APIRouter()

@router.post("/generate")
def generate(payload: dict):
    result = agent.invoke(
        {
            "prompt": payload["prompt"],
            "project_id": str(uuid4()),
            "retries": 0
        }
    )

    return result