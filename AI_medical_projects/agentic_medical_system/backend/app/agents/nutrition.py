from typing import Any, Dict
from app.agents.base import BaseAgent
from datetime import datetime

class NutritionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="NutritionAgent")

    async def process(self, input_data: Any) -> Dict[str, Any]:
        self.log_thought("Analyzing nutritional intake...")
        
        meal = input_data.get("meal", "unknown")
        calories = input_data.get("calories", 0)
        
        assessment = "Healthy choice"
        if calories > 800:
            assessment = "High calorie meal detected."
            
        return {
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "analysis": f"Analyzed meal: {meal}",
            "nutritional_assessment": assessment,
            "suggestion": "Drink water to aid digestion."
        }
