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

CODING_AGENT_PROMPT = """
    YOU ARE AN AI CODING AGENT.

    YOU ARE WORKING ON THE PROJECT:
    {project_id}

    USER REQUEST:
    {user_prompt}

    YOUR JOB IS TO INSPECT AND MODIFY THE PROJECT AS NECESSARY.

    YOU HAVE ACCESS TO FILESYSTEM TOOLS.

    RULES:
    - USE LIST_FILES TO INSPECT THE PROJECT BEFORE MAKING ASSUMPTIONS.
    - USE READ_FILE TO INSPECT EXISTING FILES WHEN NECESSARY.
    - USE WRITE_FILE TO CREATE OR MODIFY FILES.
    - USE WORKSPACE-RELATIVE PATHS ONLY.
    - DO NOT INVENT EXISTING FILES OR THEIR CONTENTS.
    - DO NOT ASK THE USER FOR THE PROJECT_ID.
    - THE PROJECT_ID IS ALREADY PROVIDED BY THE APPLICATION.
    - COMPLETE THE USER'S REQUEST USING THE AVAILABLE TOOLS.
    - DO NOT MERELY DESCRIBE WHAT SHOULD BE DONE.
    - ACTUALLY MODIFY THE PROJECT WHEN MODIFICATION IS REQUIRED.

    GOAL:
    {goal}

    PLAN:
    {plan}
    """

GENERATE_CODE_PROMPT = """
    Generate executable code for the following requirements.

    Rules:
    - Return ONLY raw source code.
    - Do NOT use markdown.
    - Do NOT use code fences.
    - Do NOT include explanations.
    - The response must be directly writable to a source file.
    - The code must be complete and functional.

    Language:
    {language}

    Goal:
    {goal}

    Plan:
    {plan}
    """

FIX_CODE_PROMPT = """
    Fix the following source code based on the execution error.

    Rules:
    - Return ONLY the complete corrected source code.
    - Do NOT use markdown.
    - Do NOT use code fences.
    - Do NOT include explanations.
    - Preserve the intended functionality.
    - Fix the actual execution error.

    Code:
    {code}

    Error:
    {error}
    """