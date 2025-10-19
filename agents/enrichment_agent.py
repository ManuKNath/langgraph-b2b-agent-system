from .base_agent import BaseAgent

class EnrichmentAgent(BaseAgent):
    def run(self, state):
        print("🧩 Enriching prospect data...")
        
        # 1. Get the current prospects
        current_prospects = state.prospects
        
        # 2. Create a NEW list with enriched data (to avoid mutation)
        enriched_prospects = []
        for p in current_prospects:
            # Create a copy to prevent mutation of the dictionary inside the list
            new_p = p.copy() 
            new_p["linkedin"] = f"https://linkedin.com/{p['company'].lower().replace(' ', '')}"
            new_p["growth_rate"] = 0.2
            enriched_prospects.append(new_p)
            
        # 3. Return the dictionary of updates
        return {"prospects": enriched_prospects}