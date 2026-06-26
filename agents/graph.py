from langgraph.graph import StateGraph
from langgraph.graph import START, END

from .state import AgentState
from .nodes import *

graph = StateGraph(AgentState)

graph.add_node("analyze", analyze_goal)
graph.add_node("plan", planner)
graph.add_node("generate", generate_code)
graph.add_node("execute", execute_code)
graph.add_node("fix", fix_code)

# ENTRY POINT
graph.add_edge(START, "analyze")

graph.add_edge("analyze", "plan")
graph.add_edge("plan", "generate")
graph.add_edge("generate", "execute")
graph.add_edge("fix", "execute")

def route(state):
    if state["error"] and state["retries"] < 3:
        return "fix"

    return END

graph.add_conditional_edges(
    "execute",
    route
)

agent = graph.compile()