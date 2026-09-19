from .coding_graph import coding_agent_graph


def coding_agent(prompt: str,project_id: str,):
    state = {
        "prompt": prompt,
        "project_id": project_id,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "status": "running",
        "output": "",
        "error": "",
        "retries": 0,
    }

    return coding_agent_graph.invoke(state)