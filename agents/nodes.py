from .llm import ask_gemini, ask_structured, ask_json
from uuid import uuid4
from tools.file_tools import save_code
from tools.docker_tools import run_python
import time
from .schemas import GoalAnalysis, Plan
from .prompts import ANALYZE_PROMPT, PLAN_PROMPT, GENERATE_CODE_PROMPT, FIX_CODE_PROMPT
from tools.code_utils import clean_code

def analyze_goal(state):

    start_time = time.time()
    prompt = ANALYZE_PROMPT.format(request=state["prompt"])

    result = ask_structured(prompt, GoalAnalysis)
    state["goal"] = result.model_dump()
    print(f"Analysis took {time.time() - start_time:.2f} seconds")
    print(state["goal"])
    return state


def planner(state):

    start_time = time.time()
    prompt = PLAN_PROMPT.format(goal=state["goal"])

    result = ask_structured(prompt, Plan)
    print(f"Planning took {time.time() - start_time:.2f} seconds")
    state["plan"] = result.model_dump()
    return state


def generate_code(state):

    start_time = time.time()
    prompt = GENERATE_CODE_PROMPT.format(goal=state["goal"], plan=state["plan"])

    code = ask_gemini(prompt)
    state["generated_code"] = clean_code(code)
    print(f"Code generation took {time.time() - start_time:.2f} seconds")
    return state
 

def execute_code(state):

    project_id = state["project_id"]
    file_path = save_code(project_id,state["generated_code"])

    state["file_path"] = file_path
    result, logs = run_python(file_path)

    if result["StatusCode"] == 0:
        state["output"] = logs
        state["error"] = ""

    else:
        state["error"] = logs

    return state


def fix_code(state):

    prompt = FIX_CODE_PROMPT.format(code=state["generated_code"], error=state["error"])

    fixed = ask_gemini(prompt)
    state["generated_code"] = clean_code(fixed)
    state["retries"] += 1
    return state