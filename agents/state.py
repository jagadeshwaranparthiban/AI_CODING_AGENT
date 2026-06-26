from typing import TypedDict

class AgentState(TypedDict):

    prompt: str
    project_id: str
    goal: str
    plan: list
    generated_code: str
    file_path: str
    output: str
    error: str
    retries: int