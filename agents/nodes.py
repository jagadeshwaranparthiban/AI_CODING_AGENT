from .llm import ask_gemini, ask_structured, ask_json
from uuid import uuid4
from tools.file_tools import save_code
from tools.docker_tools import run_python
import time
from .schemas import GoalAnalysis, Plan


def analyze_goal(state):

    start_time = time.time()
    prompt = f"""
    Analyze the request.

    Return JSON ONLY.

    {{
        "goal":"",
        "language":"",
        "requirements":[]
    }}

    Request:
    {state["prompt"]}
    """

    result = ask_structured(prompt, GoalAnalysis)
    state["goal"] = result.model_dump()
    print(f"Analysis took {time.time() - start_time:.2f} seconds")
    print(state["goal"])
    return state

# def analyze_goal(state):
#     start_time = time.time()

#     prompt = f"""
#     Analyze the user request.

#     Return:

#     Goal:
#     Language:
#     Requirements:

#     Request:
#     {state['prompt']}
#     """

#     result = ask_gemini(prompt)
#     state["goal"] = result
#     print(f"Analysis took {time.time() - start_time:.2f} seconds")
#     return state

# def planner(state):

#     start_time = time.time()
#     prompt = f"""
#     Create a step by step plan.

#     Goal:
#     {state['goal']}
#     """

#     plan = ask_gemini(prompt)
#     state["plan"] = plan
#     print(f"Planning took {time.time() - start_time:.2f} seconds")
#     return state

def planner(state):

    start_time = time.time()
    prompt = f"""
    Create an implementation plan.

    Return ONLY valid JSON.

    Do NOT wrap the response.

    Return EXACTLY this structure:

    {{
    "steps": [
        {{
        "step_number": 1,
        "description": "..."
        }}
    ]
    }}

    Goal:
    {state["goal"]}
    """

    result = ask_structured(prompt, Plan)
    print(f"Planning took {time.time() - start_time:.2f} seconds")
    state["plan"] = result.model_dump()
    return state


def generate_code(state):

    start_time = time.time()
    prompt = f"""
    Generate executable Python code.

    Rules:
    - Return ONLY raw Python source code.
    - Do NOT use markdown.
    - Do NOT use ```python.
    - Do NOT use ``` fences.
    - Do NOT include explanations.
    - The response must be directly writable to a .py file.

    Goal:
    {state["goal"]}

    Plan:
    {state["plan"]}
    """

    code = ask_gemini(prompt)
    code = (
        code.replace("```python", "")
            .replace("```py", "")
            .replace("```", "")
            .strip()
    )

    state["generated_code"] = code
    print(f"Code generation took {time.time() - start_time:.2f} seconds")
    return state
 

def execute_code(state):

    project_id = state["project_id"] or str(uuid4())
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

    prompt = f"""
    Fix the following Python code.

    Code:
    {state['generated_code']}

    Error:
    {state['error']}

    Return only code.
    """

    fixed = ask_gemini(prompt)
    state["generated_code"] = fixed
    state["retries"] += 1
    return state