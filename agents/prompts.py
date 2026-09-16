ANALYZE_PROMPT = """
    Analyze the given request.

    Return JSON ONLY.

    {{
        "goal":"",
        "language":"",
        "requirements":[]
    }}

    Request:
    {request}
    """

PLAN_PROMPT = """
    Create an implementation plan.

    Return ONLY valid JSON.

    Do NOT wrap the response.

    Return EXACTLY in this structure:

    {{
    "steps": [
        {{
        "step_number": 1,
        "description": "..."
        }}
    ]
    }}

    Goal:
    {goal}
    """

GENERATE_CODE_PROMPT = """
    Generate executable Python code.

    Rules:
    - Return ONLY raw Python source code.
    - Do NOT use markdown.
    - Do NOT use ```python.
    - Do NOT use ``` fences.
    - Do NOT include explanations.
    - The response must be directly writable to a .py file.
    - The code must be complete and functional.

    Goal:
    {goal}

    Plan:
    {plan}
    """

FIX_CODE_PROMPT = """
    Fix the following Python code.

    Code:
    {code}

    Error:
    {error}

    Return only fixed code.
    """