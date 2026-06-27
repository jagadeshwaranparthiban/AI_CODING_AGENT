from uuid import uuid4
from .graph import agent

class AgentRunner:

    def __init__(self):
        self.project_id = str(uuid4())
    
    def run(self, prompt: str):
        state = {
            "project_id": str(uuid4()),
            "prompt": prompt,
            "goal": {},
            "plan": {},
            "generated_code": "",
            "file_path": "",
            "output": "",
            "error": "",
            "retries": 0
        }

        return agent.invoke(state)

    def stream(self, prompt: str):

        state = {
            "project_id": str(uuid4()),
            "prompt": prompt,
            "goal": {},
            "plan": {},
            "generated_code": "",
            "file_path": "",
            "output": "",
            "error": "",
            "retries": 0
        }

        return agent.stream(state)