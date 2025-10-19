import json
# Import START
from langgraph.graph import StateGraph, END, START 
from pydantic import BaseModel
from typing import List, Dict, Any

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

class GraphState(BaseModel):
    query: str
    prospects: List[Dict[str, Any]] = []

def build_langgraph_from_json(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)

    graph = StateGraph(state_schema=GraphState)
    all_node_ids = {node_cfg["id"] for node_cfg in config["nodes"]}

    # Factory function to generate unique callable per node
    def make_node_fn(agent):
        def node_fn(state, agent=agent):
            return agent.run(state)
        return node_fn

    # 1️⃣ Add nodes
    for node_cfg in config["nodes"]:
        agent_class = AGENT_CLASSES[node_cfg["type"]]
        agent = agent_class(**node_cfg.get("params", {}))
        node_id = node_cfg["id"]

        node_fn = make_node_fn(agent)
        # FIX: Pass node_id as the unique key, and node_fn as the entrypoint
        graph.add_node(node_id, node_fn) 

    # 2️⃣ Add edges
    for node_cfg in config["nodes"]:
        src = node_cfg["id"]
        next_nodes = node_cfg.get("next", [])
        if not next_nodes:
            graph.add_edge(src, END)
        else:
            for dst in next_nodes:
                if dst not in all_node_ids:
                    raise ValueError(f"Edge refers to unknown node '{dst}'")
                graph.add_edge(src, dst)
    
    # 3️⃣ Add the entrypoint (The necessary addition to fix the error)
    # The first node in the list, "prospect_search", is set as the starting point.
    if config["nodes"]:
        first_node_id = config["nodes"][0]["id"]
        graph.add_edge(START, first_node_id)

    return graph.compile()