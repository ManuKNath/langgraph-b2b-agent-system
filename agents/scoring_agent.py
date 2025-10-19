from .base_agent import BaseAgent

class ScoringAgent(BaseAgent):
    def run(self, state):
        print("📊 Scoring prospects...")
        
        # 1. Get the current prospects
        current_prospects = state.prospects
        
        # 2. Create a NEW list with scored data
        scored_prospects = []
        for p in current_prospects:
            # Create a copy to prevent mutation
            new_p = p.copy()
            
            revenue_score = new_p.get("revenue", 0) / 1e8
            growth_score = new_p.get("growth_rate", 0)
            new_p["score"] = revenue_score * 0.6 + growth_score * 0.4
            
            scored_prospects.append(new_p)
            
        # 3. Return the dictionary of updates
        return {"prospects": scored_prospects}