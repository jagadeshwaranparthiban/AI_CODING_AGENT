from typing import TypedDict

class AgentState(TypedDict):

    prompt: str
    project_id: str
    goal: dict
    plan: dict
    generated_code: str
    file_path: str
    output: str
    error: str
    retries: int
    messages: list
    agent_done: bool