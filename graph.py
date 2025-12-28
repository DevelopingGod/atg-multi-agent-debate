from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
import operator

# Import nodes
from nodes.agents import scientist_node, philosopher_node
from nodes.memory import check_coherence
from nodes.judge import judge_node
import config

# Define State
class DebateState(TypedDict):
    topic: str
    messages: Annotated[List[BaseMessage], operator.add] # 'add' ensures messages are appended, not overwritten
    round_count: int
    current_speaker: str
    final_verdict: str

# Initialize Graph
workflow = StateGraph(DebateState)

# Add Nodes
workflow.add_node("Scientist", scientist_node)
workflow.add_node("Philosopher", philosopher_node)
workflow.add_node("RoundsController", check_coherence)
workflow.add_node("Judge", judge_node)

# Define Logic for Routing
def router(state):
    # If 8 rounds reached, go to Judge
    if state["round_count"] >= config.TOTAL_ROUNDS:
        return "Judge"
    
    # Alternating turns
    if state["current_speaker"] == "Scientist":
        return "Philosopher"
    else:
        return "Scientist"

# Build Edges
workflow.set_entry_point("Scientist") # Start with Scientist

workflow.add_edge("Scientist", "RoundsController")
workflow.add_edge("Philosopher", "RoundsController")

workflow.add_conditional_edges(
    "RoundsController",
    router,
    {
        "Scientist": "Scientist",
        "Philosopher": "Philosopher",
        "Judge": "Judge"
    }
)

workflow.add_edge("Judge", END)

# Compile
app = workflow.compile()

# Function to generate DAG Image
def save_dag_image():
    try:
        png_data = app.get_graph().draw_mermaid_png()
        with open("debate_dag.png", "wb") as f:
            f.write(png_data)
        print("DAG saved as debate_dag.png")
    except Exception as e:
        print(f"Could not generate DAG image (requires graphviz/mermaid): {e}")