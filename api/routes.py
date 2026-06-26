from fastapi import APIRouter
from agents.runner import AgentRunner
from uuid import uuid4

router = APIRouter()
runner = AgentRunner()

@router.post("/generate")
def generate(payload: dict):
    result = runner.run(
        prompt=payload["prompt"]
    )

    return result