from .base_agent import BaseAgent

class ProspectSearchAgent(BaseAgent):
    def run(self, state):
        # Access parameters correctly from 'self' if they were passed during agent initialization
        # The params are likely stored as instance attributes if BaseAgent handles them,
        # but let's assume they are available directly on the instance as per the constructor
        # (The workflow.json showed params being passed to the agent constructor)
        target_region = getattr(self, 'target_region', 'Unknown')
        print(f"🔍 Searching prospects in {target_region}")

        # Define the updates
        new_prospects = [
            {"company": "Acme Inc", "revenue": 50000000},
            {"company": "BetaCorp", "revenue": 150000000}
        ]
        
        # Return a dictionary of updates instead of modifying 'state' in-place
        return {"prospects": new_prospects}