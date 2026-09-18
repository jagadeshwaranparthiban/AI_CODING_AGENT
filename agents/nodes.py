from .bedrock import ask_gemini, ask_structured
from tools.file_tools import save_code
from tools.docker_tools import run_python
from .schemas import GoalAnalysis, Plan
from .prompts import ANALYZE_PROMPT, PLAN_PROMPT, GENERATE_CODE_PROMPT, FIX_CODE_PROMPT
from tools.code_utils import clean_code
from .logger import logger
from .decorators import timed
from .validation import validate_initial_state

@timed("Validate State")
def validate_state_node(state):
    validate_initial_state(state)
    logger.info("Initial state validated successfully")
    return state

@timed("Analyze Goal")
def analyze_goal(state):

    prompt = ANALYZE_PROMPT.format(request=state["prompt"])

    result = ask_structured(prompt, GoalAnalysis)
    state["goal"] = result.model_dump()
    state["language"] = result.language
    logger.info("Goal analysis: %s", state["goal"])
    return state


@timed("Plan")
def planner(state):

    prompt = PLAN_PROMPT.format(goal=state["goal"])

    result = ask_structured(prompt, Plan)
    state["plan"] = result.model_dump()
    logger.info(
        "Generated plan with %d steps",
        len(state["plan"]["steps"])
    )
    return state


@timed("Generate Code")
def generate_code(state):

    prompt = GENERATE_CODE_PROMPT.format(language=state["goal"]["language"], goal=state["goal"], plan=state["plan"])

    code = ask_gemini(prompt)
    state["generated_code"] = clean_code(code)
    logger.info("Generated code with %d characters", len(state["generated_code"]))
    return state
 
@timed("Execute Code")
def execute_code(state):

    project_id = state["project_id"]
    file_path = save_code(project_id,state["generated_code"])

    state["file_path"] = file_path
    logger.info("Saved code to %s", file_path)
    result, logs = run_python(file_path)

    if result["StatusCode"] == 0:
        state["output"] = logs
        state["error"] = ""
        logger.info("Code executed successfully with output: %s", logs)

    else:
        state["output"] = ""
        state["error"] = logs
        logger.error("Code execution failed with error: %s", logs)

    return state

@timed("Fix Code")
def fix_code(state):

    logger.info("Attempting to fix code. Retry: %d", state["retries"]+1)
    prompt = FIX_CODE_PROMPT.format(code=state["generated_code"], error=state["error"])

    fixed = ask_gemini(prompt)
    state["generated_code"] = clean_code(fixed)
    state["retries"] += 1
    return state