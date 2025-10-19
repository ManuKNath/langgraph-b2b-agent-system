from .base_agent import BaseAgent

class OutreachAgent(BaseAgent):
    def run(self, state):
        print("📧 Sending outreach emails...")
        
        current_prospects = state.prospects
        for p in current_prospects:
            print(f"Sent email to {p['company']} ({p['linkedin']})")
            
        # No actual state change, but return the prospects list back to maintain state structure
        # In LangGraph, returning the key ensures it is carried forward.
        return {"prospects": current_prospects}