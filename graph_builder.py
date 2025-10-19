import json
import os
from langgraph.graph import StateGraph, END, START
from pydantic import BaseModel
from typing import List, Dict, Any

# --- Placeholder: Load credentials from .env ---
# In a real application, you'd load environment variables here.
# Example: from dotenv import load_dotenv; load_dotenv()
# -----------------------------------------------

# Assuming these agent classes are defined in their respective files
from agents.prospect_search_agent import ProspectSearchAgent
from agents.enrichment_agent import EnrichmentAgent
from agents.scoring_agent import ScoringAgent
from agents.outreach_agent import OutreachAgent
from agents.feedback_trainer import FeedbackTrainer

AGENT_CLASSES = {
    "ProspectSearchAgent": ProspectSearchAgent,
    "EnrichmentAgent": EnrichmentAgent,
    "ScoringAgent": ScoringAgent,
    "OutreachAgent": OutreachAgent,
    "FeedbackTrainer": FeedbackTrainer
}

# 1. Graph State Definition
class GraphState(BaseModel):
    query: str
    prospects: List[Dict[str, Any]] = []
    # Placeholder: Add fields for ReAct/Conditional logic (e.g., tool_calls, next_node)

# Factory function to generate a unique callable for the node's entrypoint
def make_node_fn(agent):
    """Wraps an agent's run method to match the LangGraph node signature."""
    def node_fn(state, agent=agent):
        # The agent.run(state) method must return a dictionary of updates 
        # (e.g., {"prospects": new_list}) for the StateGraph to merge.
        return agent.run(state)
    return node_fn

# 2. Dynamic Builder Function
def build_langgraph_from_json(config_path: str):
    """
    Reads a JSON workflow configuration and constructs a LangGraph.
    
    Includes fixes for using string node IDs and setting the START edge.
    """
    # 2.1 Read and Validate workflow.json
    print(f"✅ Reading workflow from: {config_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
        
    with open(config_path, "r") as f:
        config = json.load(f)
        
    if not config.get("nodes"):
        raise ValueError("Workflow configuration must contain 'nodes'.")

    graph = StateGraph(state_schema=GraphState)
    all_node_ids = {node_cfg["id"] for node_cfg in config["nodes"]}

    # 2.2 Dynamically constructs nodes
    print("⚙️ Constructing nodes...")
    for node_cfg in config["nodes"]:
        node_id = node_cfg["id"]
        node_type = node_cfg["type"]
        
        if node_type not in AGENT_CLASSES:
             raise ValueError(f"Unknown agent type: {node_type} for node {node_id}")

        agent_class = AGENT_CLASSES[node_type]
        # Pass parameters directly to the agent constructor
        agent = agent_class(**node_cfg.get("params", {})) 
        
        node_fn = make_node_fn(agent)
        
        # FIX: Use the string 'node_id' as the unique node key
        graph.add_node(node_id, node_fn)

    # 2.3 Dynamically constructs edges (sequential structure)
    print("🔗 Adding edges (Sequential flow detected)...")
    for node_cfg in config["nodes"]:
        src = node_cfg["id"]
        next_nodes = node_cfg.get("next", [])

        # Placeholder: Conditional flow would use graph.add_conditional_edges()
        
        if not next_nodes:
            graph.add_edge(src, END)
        else:
            for dst in next_nodes:
                if dst not in all_node_ids:
                    raise ValueError(f"Edge refers to unknown node '{dst}'")
                graph.add_edge(src, dst)
    
    # FIX: Set the entrypoint (START edge)
    first_node_id = config["nodes"][0]["id"]
    graph.add_edge(START, first_node_id)
    print(f"🏁 Set entrypoint from START to: {first_node_id}")

    return graph.compile()