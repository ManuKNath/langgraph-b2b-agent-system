from .base_agent import BaseAgent

class FeedbackTrainer(BaseAgent):
    def run(self, state):
        print("🧠 Applying feedback...")
        
        # 1. Get the current prospects
        current_prospects = state.prospects
        
        # 2. Create a NEW list with updated data
        updated_prospects = []
        for p in current_prospects:
            # Create a copy to prevent mutation
            new_p = p.copy()
            # Mock: increase score slightly
            new_p["score"] = new_p.get("score", 0) + 0.05
            
            updated_prospects.append(new_p)
            
        # 3. Return the dictionary of updates
        return {"prospects": updated_prospects}