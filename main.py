from graph_builder import build_langgraph_from_json

if __name__ == "__main__":
    graph_app = build_langgraph_from_json("workflow.json")
    result = graph_app.invoke({"query": "Find B2B leads"})
    print("\n✅ Final State:", result)
