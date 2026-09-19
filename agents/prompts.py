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

    YOU ARE WORKING INSIDE THE PROJECT WORKSPACE IDENTIFIED INTERNALLY
    BY THE APPLICATION.

    USER REQUEST:
    {prompt}

    RULES:
    - ALWAYS INSPECT THE PROJECT BEFORE MAKING ASSUMPTIONS.
    - USE LIST_FILES TO INSPECT DIRECTORIES.
    - USE READ_FILE TO INSPECT EXISTING FILES.
    - USE WRITE_FILE TO CREATE OR MODIFY FILES.
    - ALWAYS USE WORKSPACE-RELATIVE PATHS.
    - NEVER PROVIDE ABSOLUTE FILESYSTEM PATHS TO TOOLS.
    - FOR THE PROJECT ROOT, USE ".".
    - NEVER PROVIDE A PROJECT_ID TO TOOLS.
    - THE APPLICATION AUTOMATICALLY SUPPLIES THE PROJECT WORKSPACE.
    - DO NOT INVENT EXISTING FILES OR THEIR CONTENTS.
    - ACTUALLY PERFORM THE REQUESTED WORK.
    - DO NOT MERELY DESCRIBE WHAT YOU WOULD DO.

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