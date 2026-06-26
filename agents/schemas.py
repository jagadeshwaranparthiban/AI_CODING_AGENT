from pydantic import BaseModel


class GoalAnalysis(BaseModel):
    goal: str
    language: str
    requirements: list[str]

class PlanStep(BaseModel):
    step_number: int
    description: str

class Plan(BaseModel):
    steps: list[PlanStep]