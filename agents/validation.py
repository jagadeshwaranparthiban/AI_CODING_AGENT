from .exceptions import StateValidationError


def validate_initial_state(state):

    if "prompt" not in state:
        raise StateValidationError(
            "Missing required field: prompt"
        )

    if not isinstance(state["prompt"], str):
        raise StateValidationError(
            "Prompt must be a string."
        )

    if not state["prompt"].strip():
        raise StateValidationError(
            "Prompt cannot be empty."
        )

    if "project_id" not in state:
        raise StateValidationError(
            "Missing required field: project_id"
        )

    if not isinstance(state["project_id"], str):
        raise StateValidationError(
            "Project ID must be a string."
        )

    if not state["project_id"].strip():
        raise StateValidationError(
            "Project ID cannot be empty."
        )

    if "retries" not in state:
        raise StateValidationError(
            "Missing required field: retries"
        )

    if not isinstance(state["retries"], int):
        raise StateValidationError(
            "Retries must be an integer."
        )

    if state["retries"] < 0:
        raise StateValidationError(
            "Retries cannot be negative."
        )

    return state